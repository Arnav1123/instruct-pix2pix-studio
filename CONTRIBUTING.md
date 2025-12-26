# Contributing to InstructPix2Pix Studio

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all experience levels.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Clear description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, GPU, Python version)
   - Error messages or logs

### Suggesting Features

1. Check existing issues and discussions
2. Describe the feature and its use case
3. Explain why it would benefit users

### Pull Requests

1. Fork the repository
2. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test your changes locally
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: add new preset for cyberpunk style"
   git commit -m "fix: resolve memory leak in batch generation"
   git commit -m "docs: update installation instructions"
   ```
6. Push and create a Pull Request

## Commit Message Format

We use Conventional Commits for clear history and automated changelog generation:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, no logic change)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add watercolor preset with custom parameters
fix: handle out-of-memory error gracefully
docs: add troubleshooting section for DirectML
refactor: simplify pipeline loading logic
```

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/instruct-pix2pix-studio.git
   cd instruct-pix2pix-studio
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements-windows.txt  # Windows
   pip install -r requirements.txt          # Linux/Mac
   ```

4. Install dev dependencies:
   ```bash
   pip install black isort flake8 pytest
   ```

## Code Style

- Use Black for formatting: `black src/ app.py`
- Sort imports with isort: `isort src/ app.py`
- Follow PEP 8 guidelines
- Add docstrings to functions and classes
- Keep functions focused and small

## Testing

Before submitting:

1. Test the application manually
2. Ensure no regressions in existing features
3. Run linting:
   ```bash
   flake8 src/ app.py
   black --check src/ app.py
   ```

## Project Structure

```
instruct-pix2pix-studio/
├── app.py              # Entry point
├── src/
│   ├── generator.py    # Image generation logic
│   ├── pipeline.py     # Model loading
│   ├── ui.py           # Gradio interface
│   ├── styles.py       # CSS styles
│   ├── presets.py      # Presets configuration
│   └── storage.py      # File management
├── .github/
│   └── workflows/      # CI/CD pipelines
└── outputs/            # Generated images (gitignored)
```

## Questions?

Open a discussion or issue if you have questions. We're happy to help!
