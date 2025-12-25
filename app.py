#!/usr/bin/env python3
"""
Qwen Image Edit Studio
Main entry point for the application
"""

from src.pipeline import load_pipeline
from src.ui import create_ui
from src.styles import CUSTOM_CSS
import gradio as gr

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
