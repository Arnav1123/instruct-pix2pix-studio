"""
Modern UI with all features
"""
import gradio as gr
from .styles import CUSTOM_CSS
from .presets import PRESETS, SETTINGS_PRESETS, get_preset_names, get_settings_preset_names, get_settings_preset
from .generator import (
    generate_image, generate_batch, randomize_seed, clear_history,
    get_system_info, estimate_time, use_as_input, add_to_favorites, export_image
)
from .storage import list_favorites


def update_time_estimate(steps):
    """Update time estimate"""
    return f"<span style='color: #06b6d4;'>{estimate_time(int(steps))}</span>"


def apply_settings_preset(preset_name):
    """Apply settings preset"""
    preset = get_settings_preset(preset_name)
    return preset["steps"], preset["guidance"], preset["image_cfg"], f"<span style='color: #94a3b8;'>{preset['description']}</span>"


def create_ui():
    """Create interface"""
    
    sys_info = get_system_info()
    
    with gr.Blocks(
        title="InstructPix2Pix Studio",
        css=CUSTOM_CSS,
        theme=gr.themes.Base(
            primary_hue="violet",
            secondary_hue="cyan",
            neutral_hue="slate",
        )
    ) as demo:
        
        # Modern Header with glassmorphism
        gr.HTML(f"""
            <div style="
                text-align: center; 
                padding: 30px 20px; 
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(6, 182, 212, 0.2) 100%);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px; 
                margin-bottom: 24px;
                position: relative;
                overflow: hidden;
            ">
                <div style="
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
                    animation: rotate 20s linear infinite;
                "></div>
                <h1 style="
                    color: white; 
                    margin: 0; 
                    font-size: 2.5em; 
                    font-weight: 700;
                    background: linear-gradient(135deg, #fff 0%, #c4b5fd 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    position: relative;
                ">InstructPix2Pix Studio</h1>
                <p style="
                    color: rgba(255,255,255,0.8); 
                    margin: 12px 0 0 0; 
                    font-size: 1.1em;
                    position: relative;
                ">AI-powered image editing</p>
                <div style="
                    margin-top: 16px; 
                    padding: 10px 20px; 
                    background: rgba(255,255,255,0.1);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                    border-radius: 12px; 
                    display: inline-block;
                    position: relative;
                ">
                    <span style="color: #06b6d4; font-weight: 500;">{sys_info['device']}</span>
                    <span style="color: rgba(255,255,255,0.5); margin: 0 10px;">|</span>
                    <span style="color: #a78bfa;">Max {sys_info['max_steps']} steps</span>
                    <span style="color: rgba(255,255,255,0.5); margin: 0 10px;">|</span>
                    <span style="color: #34d399;">{sys_info['image_size']}px</span>
                </div>
            </div>
            <style>
                @keyframes rotate {{
                    from {{ transform: rotate(0deg); }}
                    to {{ transform: rotate(360deg); }}
                }}
            </style>
            <script>
                // Clipboard paste function
                async function pasteFromClipboard() {{
                    try {{
                        const items = await navigator.clipboard.read();
                        for (const item of items) {{
                            for (const type of item.types) {{
                                if (type.startsWith('image/')) {{
                                    const blob = await item.getType(type);
                                    const file = new File([blob], 'pasted-image.png', {{ type: type }});
                                    
                                    const imageInput = document.querySelector('input[type="file"][accept*="image"]');
                                    if (imageInput) {{
                                        const dataTransfer = new DataTransfer();
                                        dataTransfer.items.add(file);
                                        imageInput.files = dataTransfer.files;
                                        imageInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    }}
                                    return true;
                                }}
                            }}
                        }}
                        alert('No image in clipboard');
                        return false;
                    }} catch (err) {{
                        console.error('Paste error:', err);
                        alert('Could not paste. Use Ctrl+V on the image field.');
                        return false;
                    }}
                }}
                
                // Global Ctrl+V for paste
                document.addEventListener('paste', async (e) => {{
                    const items = e.clipboardData?.items;
                    if (!items) return;
                    
                    for (const item of items) {{
                        if (item.type.startsWith('image/')) {{
                            const file = item.getAsFile();
                            const imageInput = document.querySelector('input[type="file"][accept*="image"]');
                            if (imageInput) {{
                                const dataTransfer = new DataTransfer();
                                dataTransfer.items.add(file);
                                imageInput.files = dataTransfer.files;
                                imageInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        }}
                    }}
                }});
            </script>
        """)
        
        with gr.Tabs():
            # ===== TAB 1: Main generation =====
            with gr.TabItem("Generate"):
                with gr.Row():
                    # Left panel - input
                    with gr.Column(scale=1):
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 0 0 12px 0;">Input Image</h3>')
                        
                        image1 = gr.Image(label="", type="numpy", height=280)
                        image2 = gr.Image(visible=False, type="numpy")
                        
                        # Image buttons
                        with gr.Row():
                            use_result_btn = gr.Button("Result to Input", size="sm")
                            paste_btn = gr.Button("Paste from Clipboard", size="sm")
                            clear_all_btn = gr.Button("Clear All", size="sm")
                        
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 15px 0 10px 0;">Prompt</h3>')
                        
                        prompt = gr.Textbox(
                            label="",
                            placeholder="Describe the changes in English...\n\nExamples:\n- make it winter with snow\n- add stylish sunglasses\n- turn into anime style",
                            lines=3
                        )
                        
                        # Prompt presets
                        gr.HTML('<p style="color: #94a3b8; margin: 12px 0 8px 0; font-weight: 500; font-size: 13px;">QUICK STYLES</p>')
                        preset_names = get_preset_names()
                        
                        with gr.Row():
                            for name in preset_names[:4]:
                                btn = gr.Button(name, size="sm")
                                btn.click(fn=lambda n=name: PRESETS[n], outputs=prompt)
                        with gr.Row():
                            for name in preset_names[4:8]:
                                btn = gr.Button(name, size="sm")
                                btn.click(fn=lambda n=name: PRESETS[n], outputs=prompt)
                        with gr.Row():
                            for name in preset_names[8:]:
                                btn = gr.Button(name, size="sm")
                                btn.click(fn=lambda n=name: PRESETS[n], outputs=prompt)
                        
                        negative_prompt = gr.Textbox(visible=False)
                        
                        # Settings
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 20px 0 12px 0;">Settings</h3>')
                        
                        # Settings presets
                        settings_preset = gr.Dropdown(
                            choices=get_settings_preset_names(),
                            value="Balanced",
                            label="Settings Preset",
                            info="Ready-made parameter combinations"
                        )
                        preset_desc = gr.HTML("<span style='color: #94a3b8;'>Optimal balance of speed and quality</span>")
                        
                        with gr.Row():
                            seed = gr.Number(
                                label="Seed", 
                                value=-1, 
                                precision=0, 
                                scale=3,
                                info="Number for reproducibility. -1 = random"
                            )
                            random_seed_btn = gr.Button("Random", size="sm", scale=1)
                        
                        steps = gr.Slider(
                            10, sys_info['max_steps'], value=20, step=1, 
                            label="Steps",
                            info="More steps = better quality, but slower"
                        )
                        time_estimate = gr.HTML(f"<span style='color: #06b6d4;'>{estimate_time(20)}</span>")
                        
                        with gr.Row():
                            image_cfg = gr.Slider(
                                1.0, 3.0, value=1.5, step=0.1, 
                                label="Image CFG",
                                info="Original preservation: higher = more similar to source"
                            )
                            guidance = gr.Slider(
                                1.0, 15.0, value=7.5, step=0.5, 
                                label="Text CFG",
                                info="Prompt strength: higher = follows instruction more closely"
                            )
                        
                        auto_save = gr.Checkbox(
                            label="Auto-save", 
                            value=True,
                            info="Save all results to outputs/ folder"
                        )
                        
                        generate_btn = gr.Button("Generate", variant="primary", size="lg")
                    
                    # Right panel - result
                    with gr.Column(scale=1):
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 0 0 12px 0;">Result</h3>')
                        
                        output_image = gr.Image(label="", type="pil", height=350)
                        
                        # Result action buttons
                        with gr.Row():
                            fav_btn = gr.Button("Add to Favorites", size="sm")
                            export_btn = gr.Button("Export", size="sm")
                        
                        with gr.Row(visible=False) as export_row:
                            export_format = gr.Radio(["PNG", "JPEG"], value="PNG", label="Format")
                            export_quality = gr.Slider(50, 100, value=95, label="JPEG Quality")
                            do_export_btn = gr.Button("Save")
                        
                        status = gr.Textbox(
                            label="Status",
                            lines=8,
                            interactive=False,
                            value="Upload an image and enter a prompt..."
                        )
                        
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 15px 0 10px 0;">History</h3>')
                        history_gallery = gr.Gallery(label="", columns=5, rows=2, height=150, object_fit="cover")
                        clear_btn = gr.Button("Clear History", size="sm")

            
            # ===== TAB 2: Batch generation =====
            with gr.TabItem("Batch"):
                gr.HTML('<h3 style="color: #e2e8f0;">Generate Multiple Variations</h3>')
                gr.HTML('<p style="color: #94a3b8;">Create multiple variants with different seeds at once. Useful for selecting the best result.</p>')
                
                with gr.Row():
                    with gr.Column():
                        batch_image = gr.Image(label="Input Image", type="numpy", height=250)
                        batch_prompt = gr.Textbox(
                            label="Prompt", 
                            lines=2,
                            info="One instruction for all variations"
                        )
                        
                        with gr.Row():
                            batch_num = gr.Slider(
                                2, 8, value=4, step=1, 
                                label="Number of Variations",
                                info="How many different results to create"
                            )
                            batch_seed = gr.Number(
                                label="Base Seed", 
                                value=-1, 
                                precision=0,
                                info="-1 = random. Variations: seed, seed+1, seed+2..."
                            )
                        
                        with gr.Row():
                            batch_img_cfg = gr.Slider(
                                1.0, 3.0, value=1.5, step=0.1, 
                                label="Image CFG",
                                info="Original preservation"
                            )
                            batch_guidance = gr.Slider(
                                1.0, 15.0, value=7.5, step=0.5, 
                                label="Text CFG",
                                info="Prompt strength"
                            )
                        
                        batch_steps = gr.Slider(
                            10, sys_info['max_steps'], value=15, step=1, 
                            label="Steps",
                            info="Less = faster, but lower quality"
                        )
                        
                        batch_btn = gr.Button("Run Batch", variant="primary", size="lg")
                    
                    with gr.Column():
                        batch_gallery = gr.Gallery(label="Results", columns=2, rows=2, height=400, object_fit="cover")
                        batch_status = gr.Textbox(label="Status", lines=2, interactive=False)
            
            # ===== TAB 3: Comparison =====
            with gr.TabItem("Compare"):
                gr.HTML('<h3 style="color: #e2e8f0;">Before/After Comparison</h3>')
                
                with gr.Row():
                    compare_before = gr.Image(label="Before (original)", type="numpy", height=350)
                    compare_after = gr.Image(label="After (result)", type="pil", height=350)
                
                gr.HTML("""
                    <p style="text-align: center; color: #94a3b8; margin-top: 15px;">
                        Upload original on the left, generation result will appear on the right automatically
                    </p>
                """)
            
            # ===== TAB 4: Favorites =====
            with gr.TabItem("Favorites"):
                gr.HTML('<h3 style="color: #e2e8f0;">Saved Images</h3>')
                
                favorites_gallery = gr.Gallery(label="", columns=4, rows=3, height=500, object_fit="cover")
                refresh_fav_btn = gr.Button("Refresh", size="sm")
                
                def load_favorites():
                    files = list_favorites()
                    return [str(f) for f in files[:20]]
                
                refresh_fav_btn.click(fn=load_favorites, outputs=favorites_gallery)
            
            # ===== TAB 5: Settings =====
            with gr.TabItem("Settings"):
                gr.HTML('<h3 style="color: #e2e8f0;">System Information</h3>')
                
                gr.HTML(f"""
                    <div style="
                        padding: 20px; 
                        background: rgba(139, 92, 246, 0.1);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(139, 92, 246, 0.2);
                        border-radius: 16px; 
                        color: #e2e8f0;
                    ">
                        <p style="margin: 8px 0;"><span style="color: #8b5cf6;">|</span> <strong>Device:</strong> {sys_info['device']}</p>
                        <p style="margin: 8px 0;"><span style="color: #06b6d4;">|</span> <strong>Max Steps:</strong> {sys_info['max_steps']}</p>
                        <p style="margin: 8px 0;"><span style="color: #10b981;">|</span> <strong>Generation Size:</strong> {sys_info['image_size']}px</p>
                        <p style="margin: 8px 0;"><span style="color: #f59e0b;">|</span> <strong>Time per Step:</strong> ~{sys_info['time_per_step']} sec</p>
                    </div>
                """)
                
                gr.HTML('<h3 style="color: #e2e8f0; margin-top: 24px;">Keyboard Shortcuts</h3>')
                gr.HTML("""
                    <div style="
                        padding: 20px; 
                        background: rgba(6, 182, 212, 0.1);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(6, 182, 212, 0.2);
                        border-radius: 16px; 
                        color: #e2e8f0;
                    ">
                        <p style="margin: 8px 0;"><strong style="color: #06b6d4;">Random Seed</strong> - Random button</p>
                        <p style="margin: 8px 0;"><strong style="color: #06b6d4;">Result to Input</strong> - for iterative editing</p>
                        <p style="margin: 8px 0;"><strong style="color: #06b6d4;">Add to Favorites</strong> - save liked results</p>
                        <p style="margin: 8px 0;"><strong style="color: #06b6d4;">Ctrl+V</strong> - paste image from clipboard</p>
                    </div>
                """)
                
                gr.HTML('<h3 style="color: #e2e8f0; margin-top: 24px;">Folders</h3>')
                gr.HTML("""
                    <div style="
                        padding: 20px; 
                        background: rgba(16, 185, 129, 0.1);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(16, 185, 129, 0.2);
                        border-radius: 16px; 
                        color: #e2e8f0;
                    ">
                        <p style="margin: 8px 0;"><strong style="color: #10b981;">outputs/</strong> - all generated images</p>
                        <p style="margin: 8px 0;"><strong style="color: #10b981;">outputs/favorites/</strong> - favorites</p>
                        <p style="margin: 8px 0;"><strong style="color: #10b981;">outputs/generation_log.json</strong> - generation history</p>
                    </div>
                """)
        
        # ===== Event handlers =====
        
        # Full clear function
        def clear_all():
            return None, None, "", [], "Cleared!"
        
        # Main generation
        random_seed_btn.click(fn=randomize_seed, outputs=seed)
        steps.change(fn=update_time_estimate, inputs=steps, outputs=time_estimate)
        
        settings_preset.change(
            fn=apply_settings_preset,
            inputs=settings_preset,
            outputs=[steps, guidance, image_cfg, preset_desc]
        )
        
        generate_btn.click(
            fn=generate_image,
            inputs=[image1, image2, prompt, negative_prompt, seed, image_cfg, guidance, steps, auto_save],
            outputs=[output_image, history_gallery, status]
        )
        
        # Result to Input
        use_result_btn.click(fn=use_as_input, inputs=output_image, outputs=image1)
        
        # Clear all
        clear_all_btn.click(
            fn=clear_all,
            outputs=[image1, output_image, prompt, history_gallery, status]
        )
        
        # Paste from clipboard (via JavaScript)
        paste_btn.click(
            fn=None,
            js="() => { pasteFromClipboard(); }"
        )
        
        # Favorites
        fav_btn.click(fn=add_to_favorites, inputs=output_image, outputs=status)
        
        # Export
        export_btn.click(fn=lambda: gr.update(visible=True), outputs=export_row)
        do_export_btn.click(
            fn=export_image,
            inputs=[output_image, export_format, export_quality],
            outputs=[gr.File(visible=False), status]
        )
        
        # Clear
        clear_btn.click(fn=clear_history, outputs=[history_gallery, status])
        
        # Batch
        batch_btn.click(
            fn=generate_batch,
            inputs=[batch_image, batch_prompt, batch_num, batch_seed, batch_img_cfg, batch_guidance, batch_steps],
            outputs=[batch_gallery, batch_status]
        )
        
        # Comparison - copy result
        output_image.change(fn=lambda x: x, inputs=output_image, outputs=compare_after)
        image1.change(fn=lambda x: x, inputs=image1, outputs=compare_before)
    
    return demo
