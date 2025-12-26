# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-12-27

### Added
- Professional CI/CD pipeline with GitHub Actions
- Automated releases with changelog generation
- Contributing guidelines
- Security scanning with Bandit
- Code quality checks with Black, isort, and flake8

### Changed
- Switched to GPU-only mode (removed CPU fallback due to impractical generation times)
- Translated all UI elements and documentation to English
- Removed emojis from codebase for cleaner professional appearance
- Improved error messages and status updates

### Removed
- CPU generation mode (was too slow to be practical)
- Device switching functionality (GPU is now required)

## [1.0.0] - 2024-01-01

### Added
- Initial release
- InstructPix2Pix model integration
- AMD DirectML support for Windows
- NVIDIA CUDA support
- Modern glassmorphism UI
- 12 quick style presets
- Batch generation with multiple seeds
- Before/after comparison view
- Favorites system
- Auto-save functionality
- Generation history logging
- Clipboard paste support
