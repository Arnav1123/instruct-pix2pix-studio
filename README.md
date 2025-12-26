# InstructPix2Pix Studio

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red?style=for-the-badge&logo=pytorch)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange?style=for-the-badge&logo=gradio)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-powered image editing with a modern glassmorphism interface**

[Features](#features) | [Installation](#installation) | [Usage](#usage) | [Screenshots](#screenshots)

</div>

---

## Features

- **AI Image Editing** — Transform images using natural language instructions
- **AMD GPU Support** — DirectML acceleration for AMD GPUs (RX 6000/7000 series)
- **NVIDIA CUDA Support** — Full CUDA acceleration for NVIDIA GPUs
- **12 Quick Presets** — Watercolor, Winter, Anime, Oil painting and more
- **Batch Generation** — Create multiple variations with different seeds
- **Before/After Comparison** — Side-by-side view of original and result
- **Favorites** — Save your best generations
- **Auto-save** — All results saved automatically with full logging
- **Smart Presets** — Fast/Balanced/Quality modes for different needs
- **Modern Dark UI** — Glassmorphism design with smooth animations

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10/11 | Windows 11 |
| **RAM** | 16 GB | 32 GB |
| **GPU** | AMD RX 5000+ / NVIDIA GTX 1060+ | AMD RX 6800+ / NVIDIA RTX 3070+ |
| **VRAM** | 8 GB | 16 GB |
| **Disk** | 10 GB free | SSD recommended |

> **Note:** GPU is required. CPU-only mode is not supported due to extremely long generation times.

## Installation

### Windows (AMD GPU)

```bash
# Clone the repository
git clone https://github.com/randomu3/instruct-pix2pix-studio.git
cd instruct-pix2pix-studio

# Run setup (creates venv and installs dependencies)
setup.bat

# Launch the application
run.bat
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv_win
venv_win\Scripts\activate

# Install dependencies
pip install -r requirements-windows.txt

# Launch
python app.py
```

## Usage

1. **Open** http://localhost:7860 in your browser
2. **Upload** an image
3. **Enter** an instruction in English (e.g., "make it winter with snow")
4. **Click** "Generate"
5. **Wait** ~20-40 seconds for the result

### Tips for Best Results

| Do | Don't |
|----------|------------|
| Use clear instructions | Vague descriptions |
| "Add sunglasses to the person" | "Make it better" |
| "Turn into watercolor painting" | "Change the style" |
| "Make the sky sunset orange" | "Different colors" |

### Parameter Guide

| Parameter | Description | Recommended |
|----------|----------|---------------|
| **Steps** | More = better quality, slower | 20-25 |
| **Image CFG** | Higher = preserves more of original | 1.3-1.8 |
| **Text CFG** | Higher = follows prompt more closely | 7-9 |
| **Seed** | -1 for random, or specific number for reproducibility | -1 |

## Screenshots

<details>
<summary>Click to expand</summary>

### Main Interface
Modern glassmorphism UI with gradient accents.

### Batch Generation
Create multiple variations at once.

### Settings
System information and parameters.

</details>

## Project Structure

```
instruct-pix2pix-studio/
├── app.py              # Entry point
├── src/
│   ├── generator.py    # Generation logic
│   ├── pipeline.py     # Model loading and device detection
│   ├── ui.py           # Gradio interface
│   ├── styles.py       # Custom CSS
│   ├── presets.py      # Prompt and settings presets
│   └── storage.py      # File saving and logging
├── outputs/            # Generated images (gitignored)
│   └── favorites/      # Favorites
├── requirements-windows.txt
├── setup.bat           # Windows setup script
└── run.bat             # Windows launch script
```

## Troubleshooting

### "DirectML not found"
```bash
pip install torch-directml
```

### "Out of memory"
- Reduce steps to 15-20
- Close other GPU-intensive applications
- Restart the application

### Slow generation
- Ensure GPU is being used (check console output)
- AMD DirectML: ~20-40 sec per image
- NVIDIA CUDA: ~5-15 sec per image

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a PR.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License — free to use, modify and distribute.

## Acknowledgments

- [InstructPix2Pix](https://github.com/timbrooks/instruct-pix2pix) — Original model by Tim Brooks
- [Hugging Face Diffusers](https://github.com/huggingface/diffusers) — Pipeline implementation
- [Gradio](https://gradio.app/) — Web interface framework

---

<div align="center">

**Made for the AI art community**

If you find this project useful, please consider giving it a star!

</div>
