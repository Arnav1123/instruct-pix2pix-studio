"""
Улучшенный UI с всеми фичами
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
    """Обновить оценку времени"""
    return f"<span style='color: #06b6d4;'>⏱️ {estimate_time(int(steps))}</span>"


def apply_settings_preset(preset_name):
    """Применить пресет настроек"""
    preset = get_settings_preset(preset_name)
    return preset["steps"], preset["guidance"], preset["image_cfg"], f"<span style='color: #94a3b8;'>{preset['description']}</span>"


def create_ui():
    """Создать интерфейс"""
    
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
        
        # Современный Header с glassmorphism
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
                ">✨ InstructPix2Pix Studio</h1>
                <p style="
                    color: rgba(255,255,255,0.8); 
                    margin: 12px 0 0 0; 
                    font-size: 1.1em;
                    position: relative;
                ">Редактируй изображения с помощью AI</p>
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
                    <span style="color: rgba(255,255,255,0.5); margin: 0 10px;">•</span>
                    <span style="color: #a78bfa;">Max {sys_info['max_steps']} шагов</span>
                    <span style="color: rgba(255,255,255,0.5); margin: 0 10px;">•</span>
                    <span style="color: #34d399;">{sys_info['image_size']}px</span>
                </div>
            </div>
            <style>
                @keyframes rotate {{
                    from {{ transform: rotate(0deg); }}
                    to {{ transform: rotate(360deg); }}
                }}
            </style>
        """)
        
        with gr.Tabs():
            # ===== TAB 1: Основная генерация =====
            with gr.TabItem("🎨 Генерация"):
                with gr.Row():
                    # Левая панель - входные данные
                    with gr.Column(scale=1):
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 0 0 12px 0;">📷 Входное изображение</h3>')
                        
                        image1 = gr.Image(label="", type="numpy", height=280)
                        image2 = gr.Image(visible=False, type="numpy")
                        
                        # Кнопка использовать результат
                        use_result_btn = gr.Button("⬅️ Использовать результат как вход", size="sm")
                        
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 15px 0 10px 0;">✏️ Промпт</h3>')
                        
                        prompt = gr.Textbox(
                            label="",
                            placeholder="Опиши изменения на английском...\n\n💡 Примеры:\n• make it winter with snow\n• add stylish sunglasses\n• turn into anime style",
                            lines=3
                        )
                        
                        # Пресеты промптов
                        gr.HTML('<p style="color: #94a3b8; margin: 12px 0 8px 0; font-weight: 500; font-size: 13px;">⚡ БЫСТРЫЕ СТИЛИ</p>')
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
                        
                        # Настройки
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 20px 0 12px 0;">⚙️ Настройки</h3>')
                        
                        # Пресеты настроек
                        settings_preset = gr.Dropdown(
                            choices=get_settings_preset_names(),
                            value="⚖️ Баланс",
                            label="Пресет настроек",
                            info="Готовые комбинации параметров"
                        )
                        preset_desc = gr.HTML("<span style='color: #94a3b8;'>Оптимальный баланс скорости и качества</span>")
                        
                        with gr.Row():
                            seed = gr.Number(
                                label="Seed", 
                                value=-1, 
                                precision=0, 
                                scale=3,
                                info="Число для воспроизводимости. -1 = случайный"
                            )
                            random_seed_btn = gr.Button("🎲", size="sm", scale=1)
                        
                        steps = gr.Slider(
                            10, sys_info['max_steps'], value=20, step=1, 
                            label="Шаги",
                            info="Больше шагов = выше качество, но дольше"
                        )
                        time_estimate = gr.HTML(f"<span style='color: #06b6d4;'>⏱️ ~{estimate_time(20)}</span>")
                        
                        with gr.Row():
                            image_cfg = gr.Slider(
                                1.0, 3.0, value=1.5, step=0.1, 
                                label="Image CFG",
                                info="Сохранение оригинала: выше = больше похоже на исходник"
                            )
                            guidance = gr.Slider(
                                1.0, 15.0, value=7.5, step=0.5, 
                                label="Text CFG",
                                info="Сила промпта: выше = точнее следует инструкции"
                            )
                        
                        auto_save = gr.Checkbox(
                            label="💾 Автосохранение", 
                            value=True,
                            info="Сохранять все результаты в папку outputs/"
                        )
                        
                        generate_btn = gr.Button("✨ Генерировать", variant="primary", size="lg")
                    
                    # Правая панель - результат
                    with gr.Column(scale=1):
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 0 0 12px 0;">🖼️ Результат</h3>')
                        
                        output_image = gr.Image(label="", type="pil", height=350)
                        
                        # Кнопки действий с результатом
                        with gr.Row():
                            fav_btn = gr.Button("⭐ В избранное", size="sm")
                            export_btn = gr.Button("💾 Экспорт", size="sm")
                        
                        with gr.Row(visible=False) as export_row:
                            export_format = gr.Radio(["PNG", "JPEG"], value="PNG", label="Формат")
                            export_quality = gr.Slider(50, 100, value=95, label="Качество JPEG")
                            do_export_btn = gr.Button("Сохранить")
                        
                        status = gr.Textbox(
                            label="📊 Статус",
                            lines=8,
                            interactive=False,
                            value="Загрузи изображение и введи промпт..."
                        )
                        
                        gr.HTML('<h3 style="color: #e2e8f0; margin: 15px 0 10px 0;">📚 История</h3>')
                        history_gallery = gr.Gallery(label="", columns=5, rows=2, height=150, object_fit="cover")
                        clear_btn = gr.Button("🗑️ Очистить историю", size="sm")

            
            # ===== TAB 2: Batch генерация =====
            with gr.TabItem("📦 Batch"):
                gr.HTML('<h3 style="color: #e2e8f0;">Генерация нескольких вариаций</h3>')
                gr.HTML('<p style="color: #94a3b8;">Создай несколько вариантов с разными seed за один раз. Полезно для выбора лучшего результата.</p>')
                
                with gr.Row():
                    with gr.Column():
                        batch_image = gr.Image(label="Входное изображение", type="numpy", height=250)
                        batch_prompt = gr.Textbox(
                            label="Промпт", 
                            lines=2,
                            info="Одна инструкция для всех вариаций"
                        )
                        
                        with gr.Row():
                            batch_num = gr.Slider(
                                2, 8, value=4, step=1, 
                                label="Количество вариаций",
                                info="Сколько разных результатов создать"
                            )
                            batch_seed = gr.Number(
                                label="Базовый seed", 
                                value=-1, 
                                precision=0,
                                info="-1 = случайный. Вариации: seed, seed+1, seed+2..."
                            )
                        
                        with gr.Row():
                            batch_img_cfg = gr.Slider(
                                1.0, 3.0, value=1.5, step=0.1, 
                                label="Image CFG",
                                info="Сохранение оригинала"
                            )
                            batch_guidance = gr.Slider(
                                1.0, 15.0, value=7.5, step=0.5, 
                                label="Text CFG",
                                info="Сила промпта"
                            )
                        
                        batch_steps = gr.Slider(
                            10, sys_info['max_steps'], value=15, step=1, 
                            label="Шаги",
                            info="Меньше = быстрее, но ниже качество"
                        )
                        
                        batch_btn = gr.Button("🚀 Запустить Batch", variant="primary", size="lg")
                    
                    with gr.Column():
                        batch_gallery = gr.Gallery(label="Результаты", columns=2, rows=2, height=400, object_fit="cover")
                        batch_status = gr.Textbox(label="Статус", lines=2, interactive=False)
            
            # ===== TAB 3: Сравнение =====
            with gr.TabItem("🔍 Сравнение"):
                gr.HTML('<h3 style="color: #e2e8f0;">Сравнение до/после</h3>')
                
                with gr.Row():
                    compare_before = gr.Image(label="До (оригинал)", type="numpy", height=350)
                    compare_after = gr.Image(label="После (результат)", type="pil", height=350)
                
                gr.HTML("""
                    <p style="text-align: center; color: #94a3b8; margin-top: 15px;">
                        💡 Загрузи оригинал слева, результат генерации появится справа автоматически
                    </p>
                """)
            
            # ===== TAB 4: Избранное =====
            with gr.TabItem("⭐ Избранное"):
                gr.HTML('<h3 style="color: #e2e8f0;">Сохранённые изображения</h3>')
                
                favorites_gallery = gr.Gallery(label="", columns=4, rows=3, height=500, object_fit="cover")
                refresh_fav_btn = gr.Button("🔄 Обновить", size="sm")
                
                def load_favorites():
                    files = list_favorites()
                    return [str(f) for f in files[:20]]
                
                refresh_fav_btn.click(fn=load_favorites, outputs=favorites_gallery)
            
            # ===== TAB 5: Настройки =====
            with gr.TabItem("⚙️ Настройки"):
                gr.HTML('<h3 style="color: #e2e8f0;">Информация о системе</h3>')
                
                gr.HTML(f"""
                    <div style="
                        padding: 20px; 
                        background: rgba(139, 92, 246, 0.1);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(139, 92, 246, 0.2);
                        border-radius: 16px; 
                        color: #e2e8f0;
                    ">
                        <p style="margin: 8px 0;"><span style="color: #8b5cf6;">●</span> <strong>Устройство:</strong> {sys_info['device']}</p>
                        <p style="margin: 8px 0;"><span style="color: #06b6d4;">●</span> <strong>Макс. шагов:</strong> {sys_info['max_steps']}</p>
                        <p style="margin: 8px 0;"><span style="color: #10b981;">●</span> <strong>Размер генерации:</strong> {sys_info['image_size']}px</p>
                        <p style="margin: 8px 0;"><span style="color: #f59e0b;">●</span> <strong>Время на шаг:</strong> ~{sys_info['time_per_step']} сек</p>
                    </div>
                """)
                
                gr.HTML('<h3 style="color: #e2e8f0; margin-top: 24px;">Горячие клавиши</h3>')
                gr.HTML("""
                    <div style="
                        padding: 20px; 
                        background: rgba(6, 182, 212, 0.1);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(6, 182, 212, 0.2);
                        border-radius: 16px; 
                        color: #e2e8f0;
                    ">
                        <p style="margin: 8px 0;">🎲 <strong style="color: #06b6d4;">Случайный seed</strong> — кнопка 🎲</p>
                        <p style="margin: 8px 0;">⬅️ <strong style="color: #06b6d4;">Результат → Вход</strong> — для итеративного редактирования</p>
                        <p style="margin: 8px 0;">⭐ <strong style="color: #06b6d4;">В избранное</strong> — сохранить понравившийся результат</p>
                    </div>
                """)
                
                gr.HTML('<h3 style="color: #e2e8f0; margin-top: 24px;">Папки</h3>')
                gr.HTML("""
                    <div style="
                        padding: 20px; 
                        background: rgba(16, 185, 129, 0.1);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(16, 185, 129, 0.2);
                        border-radius: 16px; 
                        color: #e2e8f0;
                    ">
                        <p style="margin: 8px 0;">📁 <strong style="color: #10b981;">outputs/</strong> — все сгенерированные изображения</p>
                        <p style="margin: 8px 0;">⭐ <strong style="color: #10b981;">outputs/favorites/</strong> — избранное</p>
                        <p style="margin: 8px 0;">📋 <strong style="color: #10b981;">outputs/generation_log.json</strong> — история генераций</p>
                    </div>
                """)
        
        # ===== Event handlers =====
        
        # Основная генерация
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
        
        # Результат → Вход
        use_result_btn.click(fn=use_as_input, inputs=output_image, outputs=image1)
        
        # Избранное
        fav_btn.click(fn=add_to_favorites, inputs=output_image, outputs=status)
        
        # Экспорт
        export_btn.click(fn=lambda: gr.update(visible=True), outputs=export_row)
        do_export_btn.click(
            fn=export_image,
            inputs=[output_image, export_format, export_quality],
            outputs=[gr.File(visible=False), status]
        )
        
        # Очистка
        clear_btn.click(fn=clear_history, outputs=[history_gallery, status])
        
        # Batch
        batch_btn.click(
            fn=generate_batch,
            inputs=[batch_image, batch_prompt, batch_num, batch_seed, batch_img_cfg, batch_guidance, batch_steps],
            outputs=[batch_gallery, batch_status]
        )
        
        # Сравнение - копируем результат
        output_image.change(fn=lambda x: x, inputs=output_image, outputs=compare_after)
        image1.change(fn=lambda x: x, inputs=image1, outputs=compare_before)
    
    return demo
