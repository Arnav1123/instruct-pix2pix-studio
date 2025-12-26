"""
Image generation module with error protection
"""
import torch
import gc
import time
import traceback
import gradio as gr
from PIL import Image
from .pipeline import get_pipeline, clear_memory, get_device_type, get_device
from .storage import save_image, save_to_favorites, log_generation

# Generation history (in memory)
_generation_history = []
_is_generating = False

# Quality settings by device type
MAX_STEPS = {
    "cuda": 50,
    "directml": 35,
}

IMAGE_SIZE = {
    "cuda": 512,
    "directml": 448,
}

TIME_PER_STEP = {
    "cuda": 0.3,
    "directml": 1.0,
}


def get_system_info():
    """Get system information"""
    device_type = get_device_type()
    mode_names = {
        "cuda": "CUDA/ROCm GPU",
        "directml": "DirectML (AMD)",
    }
    return {
        "device": mode_names.get(device_type, "Unknown"),
        "device_type": device_type,
        "max_steps": MAX_STEPS.get(device_type, 25),
        "image_size": IMAGE_SIZE.get(device_type, 448),
        "time_per_step": TIME_PER_STEP.get(device_type, 1.0),
    }


def estimate_time(steps):
    """Estimate generation time"""
    device_type = get_device_type()
    time_per_step = TIME_PER_STEP.get(device_type, 1.0)
    total_seconds = steps * time_per_step + 5
    
    if total_seconds < 60:
        return f"~{int(total_seconds)} sec"
    else:
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"~{minutes} min {seconds} sec"


def safe_generate(func):
    """Decorator for safe generation"""
    def wrapper(*args, **kwargs):
        global _is_generating
        
        if _is_generating:
            return None, _generation_history[-10:] if _generation_history else [], "Generation already in progress, please wait..."
        
        _is_generating = True
        try:
            return func(*args, **kwargs)
        except torch.cuda.OutOfMemoryError:
            clear_memory()
            return None, _generation_history[-10:] if _generation_history else [], "Out of GPU memory! Try reducing steps."
        except MemoryError:
            clear_memory()
            return None, _generation_history[-10:] if _generation_history else [], "Out of RAM!"
        except Exception as e:
            clear_memory()
            print(f"[Error]\n{traceback.format_exc()}")
            return None, _generation_history[-10:] if _generation_history else [], f"Error: {str(e)[:200]}"
        finally:
            _is_generating = False
            clear_memory()
    
    return wrapper


@safe_generate
def generate_image(
    image1, image2, prompt, negative_prompt, seed,
    image_guidance_scale, guidance_scale, num_inference_steps,
    auto_save=True,
    progress=gr.Progress(track_tqdm=True)
):
    """Main generation function"""
    global _generation_history
    
    start_time = time.time()
    
    if not prompt.strip():
        return None, _generation_history[-10:] if _generation_history else [], "Please enter a prompt"
    
    # Get input image
    if image1 is not None:
        input_image = Image.fromarray(image1).convert("RGB")
    elif image2 is not None:
        input_image = Image.fromarray(image2).convert("RGB")
    else:
        return None, _generation_history[-10:] if _generation_history else [], "Please upload an image"
    
    # Device parameters
    device_type = get_device_type()
    image_size = IMAGE_SIZE.get(device_type, 448)
    max_steps = MAX_STEPS.get(device_type, 25)
    time_per_step = TIME_PER_STEP.get(device_type, 1.0)
    
    mode_names = {
        "cuda": "CUDA/ROCm GPU",
        "directml": "DirectML (AMD)",
    }
    mode_name = mode_names.get(device_type, "Unknown")
    
    # Resize
    original_size = input_image.size
    input_image = input_image.resize((image_size, image_size), Image.Resampling.LANCZOS)
    
    # Limit steps
    safe_steps = min(int(num_inference_steps), max_steps)
    
    progress(0.05, desc=f"Preparing ({mode_name})...")
    clear_memory()
    time.sleep(0.3)
    
    # Seed
    actual_seed = seed if seed >= 0 else torch.randint(0, 2**32 - 1, (1,)).item()
    generator = torch.Generator("cpu").manual_seed(actual_seed)
    
    progress(0.1, desc=f"Generating ({safe_steps} steps)...")
    
    pipeline = get_pipeline()
    
    # Progress callback
    def progress_callback(pipe, step, timestep, callback_kwargs):
        remaining = (safe_steps - step) * time_per_step
        pct = 0.1 + (step / safe_steps) * 0.85
        progress(pct, desc=f"Step {step}/{safe_steps} | ~{int(remaining)} sec")
        return callback_kwargs
    
    # Generation
    if device_type == "cuda":
        with torch.inference_mode():
            with torch.cuda.amp.autocast(dtype=torch.float16):
                output = pipeline(
                    prompt=prompt,
                    image=input_image,
                    num_inference_steps=safe_steps,
                    guidance_scale=guidance_scale,
                    image_guidance_scale=image_guidance_scale,
                    generator=generator,
                    callback_on_step_end=progress_callback,
                )
    else:
        with torch.no_grad():
            output = pipeline(
                prompt=prompt,
                image=input_image,
                num_inference_steps=safe_steps,
                guidance_scale=guidance_scale,
                image_guidance_scale=image_guidance_scale,
                generator=generator,
                callback_on_step_end=progress_callback,
            )
    
    progress(0.98, desc="Finalizing...")
    
    result_image = output.images[0]
    elapsed_time = time.time() - start_time
    
    # Auto-save
    saved_path = None
    if auto_save:
        saved_path = save_image(result_image)
    
    # Logging
    log_generation({
        "prompt": prompt,
        "seed": actual_seed,
        "steps": safe_steps,
        "guidance": guidance_scale,
        "image_cfg": image_guidance_scale,
        "time": round(elapsed_time, 1),
        "device": mode_name,
        "saved_path": saved_path
    })
    
    # History
    _generation_history.append(result_image)
    if len(_generation_history) > 20:
        _generation_history = _generation_history[-20:]
    
    progress(1.0, desc="Done!")
    
    status = f"""GENERATION COMPLETE

Time: {elapsed_time:.1f} sec
Seed: {actual_seed}
Prompt: {prompt[:60]}{'...' if len(prompt) > 60 else ''}

Parameters: {safe_steps} steps | CFG {guidance_scale} | ImgCFG {image_guidance_scale}
Device: {mode_name} ({image_size}px)
Saved: {saved_path if saved_path else 'No'}"""
    
    return result_image, _generation_history[-10:], status


def generate_batch(
    image, prompt, num_variations, base_seed,
    image_guidance_scale, guidance_scale, num_inference_steps,
    progress=gr.Progress()
):
    """Generate multiple variations with different seeds"""
    global _generation_history
    
    if image is None:
        return [], "Please upload an image"
    
    if not prompt.strip():
        return [], "Please enter a prompt"
    
    results = []
    num_variations = min(int(num_variations), 8)  # Max 8
    
    for i in range(num_variations):
        progress((i / num_variations), desc=f"Generating {i+1}/{num_variations}...")
        
        seed = base_seed + i if base_seed >= 0 else -1
        
        result, _, _ = generate_image(
            image, None, prompt, "", seed,
            image_guidance_scale, guidance_scale, num_inference_steps,
            auto_save=True,
            progress=progress
        )
        
        if result is not None:
            results.append(result)
    
    progress(1.0, desc="Batch complete!")
    
    return results, f"Generated {len(results)} images"


def use_as_input(image):
    """Use result as input image"""
    if image is None:
        return None
    return image


def add_to_favorites(image):
    """Add to favorites"""
    if image is None:
        return "No image to save"
    
    try:
        if hasattr(image, 'save'):
            path = save_to_favorites(image)
        else:
            img = Image.fromarray(image)
            path = save_to_favorites(img)
        return f"Saved to favorites: {path}"
    except Exception as e:
        return f"Error: {e}"


def export_image(image, format_choice, quality):
    """Export image with format selection"""
    if image is None:
        return None, "No image to export"
    
    try:
        if hasattr(image, 'save'):
            img = image
        else:
            img = Image.fromarray(image)
        
        fmt = "PNG" if format_choice == "PNG" else "JPEG"
        path = save_image(img, format=fmt, quality=int(quality))
        return path, f"Saved: {path}"
    except Exception as e:
        return None, f"Error: {e}"


def randomize_seed():
    """Random seed"""
    return torch.randint(0, 2**32 - 1, (1,)).item()


def clear_history():
    """Clear history"""
    global _generation_history
    _generation_history = []
    clear_memory()
    return [], "History cleared"


def get_history():
    """Get current history"""
    return _generation_history[-10:] if _generation_history else []
