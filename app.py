#!/usr/bin/env python3
"""
InstructPix2Pix Studio
AI-powered image editing application
"""

from src.pipeline import load_pipeline
from src.ui import create_ui


def main():
    # Pre-load the pipeline
    load_pipeline()
    
    # Create and launch UI
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
