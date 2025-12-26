"""
Pipeline loading and device management
GPU-only mode (CUDA/DirectML)
"""
import torch
import gc
import os
from diffusers import StableDiffusionInstructPix2PixPipeline

_pipeline = None
_device = None
_device_type = None  # "cuda", "directml"
_available_devices = []


def detect_available_devices():
    """Detect all available GPU devices"""
    global _available_devices
    _available_devices = []
    
    # Check CUDA
    if torch.cuda.is_available():
        _available_devices.append("cuda")
    
    # Check DirectML
    try:
        import torch_directml
        torch_directml.device()
        _available_devices.append("directml")
    except:
        pass
    
    return _available_devices


def get_available_devices():
    """Get list of available devices"""
    global _available_devices
    if not _available_devices:
        detect_available_devices()
    return _available_devices


def get_device():
    """Determine best device: CUDA/ROCm > DirectML"""
    global _device, _device_type
    if _device is not None:
        return _device
    
    # 1. Check CUDA (NVIDIA) or ROCm (AMD Linux)
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"[GPU] Found: {device_name} ({vram:.1f}GB VRAM)")
        _device = torch.device("cuda")
        _device_type = "cuda"
        return _device
    
    # 2. Check DirectML (AMD Windows)
    try:
        import torch_directml
        dml_device = torch_directml.device()
        print(f"[GPU] DirectML device found (AMD Windows)")
        _device = dml_device
        _device_type = "directml"
        return _device
    except ImportError:
        pass
    except Exception as e:
        print(f"[Warning] DirectML error: {e}")
    
    # 3. No GPU found - raise error
    raise RuntimeError(
        "No GPU found! This application requires a GPU.\n"
        "Supported: NVIDIA (CUDA), AMD (DirectML on Windows, ROCm on Linux)\n"
        "Please install appropriate drivers and PyTorch with GPU support."
    )


def get_device_type():
    """Returns device type: cuda, directml"""
    global _device_type
    if _device_type is None:
        get_device()
    return _device_type


def clear_memory():
    """Aggressive memory cleanup"""
    gc.collect()
    gc.collect()
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()


def load_pipeline():
    """Load InstructPix2Pix pipeline - GPU only"""
    global _pipeline

    if _pipeline is not None:
        return _pipeline
    
    device = get_device()
    device_type = get_device_type()
    
    print("[Pipeline] Loading InstructPix2Pix...")
    print("[Pipeline] First load downloads ~5GB model, please wait...")
    
    clear_memory()
    
    try:
        if device_type == "cuda":
            # CUDA/ROCm mode
            print("[Pipeline] Loading on CUDA/ROCm GPU (float16)...")
            
            _pipeline = StableDiffusionInstructPix2PixPipeline.from_pretrained(
                "timbrooks/instruct-pix2pix",
                torch_dtype=torch.float16,
                safety_checker=None,
                low_cpu_mem_usage=True,
            )
            _pipeline = _pipeline.to(device)
            
            _pipeline.enable_attention_slicing("auto")
            _pipeline.enable_vae_slicing()
            
            try:
                _pipeline.enable_vae_tiling()
                print("[Pipeline] VAE tiling enabled")
            except Exception:
                pass
            
            print("[Pipeline] Ready on GPU (~5-15 sec per image)")
            
        elif device_type == "directml":
            # DirectML mode (AMD Windows) - float32 required
            print("[Pipeline] Loading on DirectML (AMD Windows, float32)...")
            
            _pipeline = StableDiffusionInstructPix2PixPipeline.from_pretrained(
                "timbrooks/instruct-pix2pix",
                torch_dtype=torch.float32,
                safety_checker=None,
                low_cpu_mem_usage=True,
            )
            _pipeline = _pipeline.to(device)
            
            _pipeline.enable_attention_slicing(1)
            
            print("[Pipeline] Ready on DirectML (~20-40 sec per image)")
            
    except Exception as e:
        print(f"[Error] Failed to load pipeline: {e}")
        raise RuntimeError(f"Failed to load pipeline on GPU: {e}")
    
    _pipeline.set_progress_bar_config(disable=None)
    
    return _pipeline


def get_pipeline():
    """Get the cached pipeline instance"""
    global _pipeline
    if _pipeline is None:
        return load_pipeline()
    return _pipeline


def is_gpu_mode():
    """Check if running on GPU (always True in GPU-only mode)"""
    return True
