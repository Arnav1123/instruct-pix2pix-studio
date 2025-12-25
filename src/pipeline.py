import torch
import gc
import os
from diffusers import StableDiffusionInstructPix2PixPipeline

_pipeline = None
_device = None
_device_type = None  # "cuda", "directml", "cpu"

# Настройки для Ryzen 5950X (16 ядер / 32 потока)
NUM_THREADS = 28
NUM_INTEROP = 12


def get_device():
    """Определяем лучшее устройство: CUDA/ROCm > DirectML > CPU"""
    global _device, _device_type
    if _device is not None:
        return _device
    
    # 1. Проверяем CUDA (NVIDIA) или ROCm (AMD Linux)
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"🎮 GPU найден: {device_name} ({vram:.1f}GB VRAM)")
        _device = torch.device("cuda")
        _device_type = "cuda"
        return _device
    
    # 2. Проверяем DirectML (AMD Windows)
    try:
        import torch_directml
        dml_device = torch_directml.device()
        print(f"🎮 DirectML GPU найден (AMD Windows)")
        _device = dml_device
        _device_type = "directml"
        return _device
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️ DirectML ошибка: {e}")
    
    # 3. Fallback на CPU
    print("💻 GPU не найден, используем CPU (Ryzen 5950X)")
    _device = torch.device("cpu")
    _device_type = "cpu"
    return _device


def get_device_type():
    """Возвращает тип устройства: cuda, directml, cpu"""
    global _device_type
    if _device_type is None:
        get_device()
    return _device_type


def setup_cpu_optimizations():
    """Настройка PyTorch для Ryzen 5950X"""
    torch.set_num_threads(NUM_THREADS)
    torch.set_num_interop_threads(NUM_INTEROP)
    
    os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
    os.environ["MKL_NUM_THREADS"] = str(NUM_THREADS)
    
    print(f"🔧 CPU: {NUM_THREADS} threads, {NUM_INTEROP} interop")


def clear_memory():
    """Агрессивная очистка памяти"""
    gc.collect()
    gc.collect()
    
    # Очистка GPU памяти если доступна
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()


def load_pipeline():
    """Load InstructPix2Pix pipeline - GPU preferred, CPU fallback"""
    global _pipeline

    if _pipeline is not None:
        return _pipeline
    
    device = get_device()
    device_type = get_device_type()
    
    print("🚀 Loading InstructPix2Pix pipeline...")
    print("⏳ First load downloads ~5GB model, please wait...")
    
    # Всегда настраиваем CPU (для fallback и data loading)
    setup_cpu_optimizations()
    clear_memory()
    
    try:
        if device_type == "cuda":
            # CUDA/ROCm режим
            print("🎮 Загрузка на CUDA/ROCm GPU (float16)...")
            
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
                print("✅ VAE tiling включен")
            except Exception:
                pass
            
            print("✅ Pipeline на GPU! (~5-15 сек на изображение)")
            
        elif device_type == "directml":
            # DirectML режим (AMD Windows) - float32 обязателен!
            print("🎮 Загрузка на DirectML (AMD Windows, float32)...")
            
            _pipeline = StableDiffusionInstructPix2PixPipeline.from_pretrained(
                "timbrooks/instruct-pix2pix",
                torch_dtype=torch.float32,  # DirectML не поддерживает float16 полностью
                safety_checker=None,
                low_cpu_mem_usage=True,
            )
            _pipeline = _pipeline.to(device)
            
            # Минимальные оптимизации для DirectML
            _pipeline.enable_attention_slicing(1)
            
            print("✅ Pipeline на DirectML! (~20-40 сек на изображение)")
            
        else:
            # CPU режим
            print("💻 Загрузка на CPU...")
            
            _pipeline = StableDiffusionInstructPix2PixPipeline.from_pretrained(
                "timbrooks/instruct-pix2pix",
                torch_dtype=torch.float32,
                safety_checker=None,
                low_cpu_mem_usage=True,
            )
            
            _pipeline.enable_attention_slicing(1)
            _pipeline.enable_vae_slicing()
            
            print("✅ Pipeline на CPU (~1-2 мин на изображение)")
            
    except Exception as e:
        print(f"⚠️ Ошибка загрузки: {e}")
        print("🔄 Пробуем CPU fallback...")
        
        clear_memory()
        _pipeline = StableDiffusionInstructPix2PixPipeline.from_pretrained(
            "timbrooks/instruct-pix2pix",
            torch_dtype=torch.float32,
            safety_checker=None,
            low_cpu_mem_usage=True,
        )
        _pipeline.enable_attention_slicing(1)
        _pipeline.enable_vae_slicing()
        
        global _device_type
        _device_type = "cpu"
        print("✅ Pipeline на CPU (fallback)")
    
    _pipeline.set_progress_bar_config(disable=None)
    
    return _pipeline


def get_pipeline():
    """Get the cached pipeline instance"""
    global _pipeline
    if _pipeline is None:
        return load_pipeline()
    return _pipeline


def is_gpu_mode():
    """Проверка работает ли на GPU"""
    return get_device_type() in ("cuda", "directml")
