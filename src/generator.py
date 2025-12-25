"""
Модуль генерации изображений с защитой от падений
"""
import torch
import gc
import time
import traceback
import gradio as gr
from PIL import Image
from .pipeline import get_pipeline, clear_memory, is_gpu_mode, get_device_type, get_device
from .storage import save_image, save_to_favorites, log_generation

# История генераций (в памяти)
_generation_history = []
_is_generating = False
_generation_queue = []

# Настройки качества по типу устройства
MAX_STEPS = {
    "cuda": 50,
    "directml": 35,
    "cpu": 30,
}

IMAGE_SIZE = {
    "cuda": 512,
    "directml": 448,
    "cpu": 384,
}

TIME_PER_STEP = {
    "cuda": 0.3,
    "directml": 1.0,
    "cpu": 3.0,
}


def get_system_info():
    """Получить информацию о системе"""
    device_type = get_device_type()
    mode_names = {
        "cuda": "🎮 CUDA/ROCm GPU",
        "directml": "🎮 DirectML (AMD)",
        "cpu": "💻 CPU (Ryzen)"
    }
    return {
        "device": mode_names.get(device_type, "Unknown"),
        "device_type": device_type,
        "max_steps": MAX_STEPS.get(device_type, 25),
        "image_size": IMAGE_SIZE.get(device_type, 384),
        "time_per_step": TIME_PER_STEP.get(device_type, 3.0),
    }


def estimate_time(steps):
    """Оценка времени генерации"""
    device_type = get_device_type()
    time_per_step = TIME_PER_STEP.get(device_type, 3.0)
    total_seconds = steps * time_per_step + 5
    
    if total_seconds < 60:
        return f"~{int(total_seconds)} сек"
    else:
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"~{minutes} мин {seconds} сек"


def safe_generate(func):
    """Декоратор для безопасной генерации"""
    def wrapper(*args, **kwargs):
        global _is_generating
        
        if _is_generating:
            return None, _generation_history[-10:] if _generation_history else [], "⚠️ Генерация уже идёт, подожди..."
        
        _is_generating = True
        try:
            return func(*args, **kwargs)
        except torch.cuda.OutOfMemoryError:
            clear_memory()
            return None, _generation_history[-10:] if _generation_history else [], "❌ Недостаточно памяти GPU!"
        except MemoryError:
            clear_memory()
            return None, _generation_history[-10:] if _generation_history else [], "❌ Недостаточно RAM!"
        except Exception as e:
            clear_memory()
            print(f"❌ Ошибка:\n{traceback.format_exc()}")
            return None, _generation_history[-10:] if _generation_history else [], f"❌ Ошибка: {str(e)[:200]}"
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
    """Основная функция генерации"""
    global _generation_history
    
    start_time = time.time()
    
    if not prompt.strip():
        return None, _generation_history[-10:] if _generation_history else [], "⚠️ Введи промпт"
    
    # Получаем входное изображение
    if image1 is not None:
        input_image = Image.fromarray(image1).convert("RGB")
    elif image2 is not None:
        input_image = Image.fromarray(image2).convert("RGB")
    else:
        return None, _generation_history[-10:] if _generation_history else [], "⚠️ Загрузи изображение"
    
    # Параметры устройства
    device_type = get_device_type()
    image_size = IMAGE_SIZE.get(device_type, 384)
    max_steps = MAX_STEPS.get(device_type, 25)
    time_per_step = TIME_PER_STEP.get(device_type, 3.0)
    
    mode_names = {
        "cuda": "CUDA/ROCm GPU",
        "directml": "DirectML (AMD)",
        "cpu": "CPU (Ryzen 5950X)"
    }
    mode_name = mode_names.get(device_type, "Unknown")
    
    # Resize
    original_size = input_image.size
    input_image = input_image.resize((image_size, image_size), Image.Resampling.LANCZOS)
    
    # Ограничиваем шаги
    safe_steps = min(int(num_inference_steps), max_steps)
    
    progress(0.05, desc=f"🔧 Подготовка ({mode_name})...")
    clear_memory()
    time.sleep(0.3)
    
    # Seed
    actual_seed = seed if seed >= 0 else torch.randint(0, 2**32 - 1, (1,)).item()
    generator = torch.Generator("cpu").manual_seed(actual_seed)
    
    progress(0.1, desc=f"🚀 Генерация ({safe_steps} шагов)...")
    
    pipeline = get_pipeline()
    
    # Callback прогресса
    def progress_callback(pipe, step, timestep, callback_kwargs):
        remaining = (safe_steps - step) * time_per_step
        pct = 0.1 + (step / safe_steps) * 0.85
        progress(pct, desc=f"🎨 Шаг {step}/{safe_steps} | ~{int(remaining)} сек")
        return callback_kwargs
    
    # Генерация
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
    
    progress(0.98, desc="✨ Финализация...")
    
    result_image = output.images[0]
    elapsed_time = time.time() - start_time
    
    # Автосохранение
    saved_path = None
    if auto_save:
        saved_path = save_image(result_image)
    
    # Логирование
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
    
    # История
    _generation_history.append(result_image)
    if len(_generation_history) > 20:
        _generation_history = _generation_history[-20:]
    
    progress(1.0, desc="✅ Готово!")
    
    status = f"""✅ ГЕНЕРАЦИЯ ЗАВЕРШЕНА!

⏱️ Время: {elapsed_time:.1f} сек
🎲 Seed: {actual_seed}
📝 Промпт: {prompt[:60]}{'...' if len(prompt) > 60 else ''}

⚙️ Параметры: {safe_steps} шагов | CFG {guidance_scale} | ImgCFG {image_guidance_scale}
🎮 Режим: {mode_name} ({image_size}px)
💾 Сохранено: {saved_path if saved_path else 'Нет'}"""
    
    return result_image, _generation_history[-10:], status


def generate_batch(
    image, prompt, num_variations, base_seed,
    image_guidance_scale, guidance_scale, num_inference_steps,
    progress=gr.Progress()
):
    """Генерация нескольких вариаций с разными seed"""
    global _generation_history
    
    if image is None:
        return [], "⚠️ Загрузи изображение"
    
    if not prompt.strip():
        return [], "⚠️ Введи промпт"
    
    results = []
    num_variations = min(int(num_variations), 8)  # Максимум 8
    
    for i in range(num_variations):
        progress((i / num_variations), desc=f"🎨 Генерация {i+1}/{num_variations}...")
        
        seed = base_seed + i if base_seed >= 0 else -1
        
        result, _, _ = generate_image(
            image, None, prompt, "", seed,
            image_guidance_scale, guidance_scale, num_inference_steps,
            auto_save=True,
            progress=progress
        )
        
        if result is not None:
            results.append(result)
    
    progress(1.0, desc="✅ Batch готов!")
    
    return results, f"✅ Сгенерировано {len(results)} изображений"


def use_as_input(image):
    """Использовать результат как входное изображение"""
    if image is None:
        return None
    return image


def add_to_favorites(image):
    """Добавить в избранное"""
    if image is None:
        return "⚠️ Нет изображения"
    
    try:
        if hasattr(image, 'save'):
            path = save_to_favorites(image)
        else:
            img = Image.fromarray(image)
            path = save_to_favorites(img)
        return f"⭐ Сохранено в избранное: {path}"
    except Exception as e:
        return f"❌ Ошибка: {e}"


def export_image(image, format_choice, quality):
    """Экспорт изображения с выбором формата"""
    if image is None:
        return None, "⚠️ Нет изображения"
    
    try:
        if hasattr(image, 'save'):
            img = image
        else:
            img = Image.fromarray(image)
        
        fmt = "PNG" if format_choice == "PNG" else "JPEG"
        path = save_image(img, format=fmt, quality=int(quality))
        return path, f"💾 Сохранено: {path}"
    except Exception as e:
        return None, f"❌ Ошибка: {e}"


def randomize_seed():
    """Случайный seed"""
    return torch.randint(0, 2**32 - 1, (1,)).item()


def clear_history():
    """Очистить историю"""
    global _generation_history
    _generation_history = []
    clear_memory()
    return [], "🗑️ История очищена"


def get_history():
    """Получить текущую историю"""
    return _generation_history[-10:] if _generation_history else []
