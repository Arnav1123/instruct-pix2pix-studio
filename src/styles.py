"""
Modern glassmorphism design with animations
"""

CUSTOM_CSS = """
/* ===== MAIN VARIABLES ===== */
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-card: rgba(25, 25, 35, 0.8);
    --bg-glass: rgba(255, 255, 255, 0.05);
    --border-glass: rgba(255, 255, 255, 0.1);
    --accent-primary: #8b5cf6;
    --accent-secondary: #06b6d4;
    --accent-gradient: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
    --accent-glow: 0 0 30px rgba(139, 92, 246, 0.3);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
}

/* ===== GLOBAL STYLES ===== */
.gradio-container {
    background: var(--bg-primary) !important;
    background-image: 
        radial-gradient(ellipse at top left, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at bottom right, rgba(6, 182, 212, 0.1) 0%, transparent 50%) !important;
    min-height: 100vh;
}

.dark {
    --body-background-fill: var(--bg-primary) !important;
}

/* Hide footer */
footer { display: none !important; }

/* ===== GLASSMORPHISM CARDS ===== */
.gr-panel, .gr-box, .gr-form {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-lg) !important;
}

/* ===== TABS ===== */
.tabs {
    background: transparent !important;
    border: none !important;
}

.tab-nav {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: var(--radius-xl) !important;
    padding: 6px !important;
    border: 1px solid var(--border-glass) !important;
    gap: 4px !important;
}

.tab-nav button {
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.tab-nav button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    color: var(--text-primary) !important;
}

.tab-nav button.selected {
    background: var(--accent-gradient) !important;
    color: white !important;
    box-shadow: var(--accent-glow) !important;
}

/* ===== INPUTS AND TEXT FIELDS ===== */
textarea, input[type="text"], input[type="number"], .gr-text-input {
    background: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
}

textarea:focus, input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2), var(--accent-glow) !important;
    outline: none !important;
}

textarea::placeholder, input::placeholder {
    color: var(--text-muted) !important;
}

/* ===== SLIDERS ===== */
input[type="range"] {
    accent-color: var(--accent-primary) !important;
}

.gr-slider input[type="range"] {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    height: 6px !important;
}

.gr-slider input[type="range"]::-webkit-slider-thumb {
    background: var(--accent-gradient) !important;
    border: 2px solid white !important;
    width: 18px !important;
    height: 18px !important;
    border-radius: 50% !important;
    box-shadow: var(--accent-glow) !important;
    cursor: pointer !important;
}

/* ===== BUTTONS ===== */
.gr-button {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}

.gr-button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: var(--accent-primary) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
}

.gr-button:active {
    transform: translateY(0) !important;
}

/* Primary generate button */
.gr-button.primary {
    background: var(--accent-gradient) !important;
    border: none !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 14px 28px !important;
    box-shadow: var(--accent-glow) !important;
}

.gr-button.primary:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(139, 92, 246, 0.4) !important;
}

/* Pulse animation for button */
.gr-button.primary::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* ===== IMAGES ===== */
.gr-image, .image-container {
    background: var(--bg-glass) !important;
    border: 2px dashed var(--border-glass) !important;
    border-radius: var(--radius-lg) !important;
    transition: all 0.3s ease !important;
    overflow: hidden !important;
}

.gr-image:hover {
    border-color: var(--accent-primary) !important;
    box-shadow: var(--accent-glow) !important;
}

.gr-image img {
    border-radius: var(--radius-md) !important;
}

/* ===== GALLERY ===== */
.gr-gallery {
    background: transparent !important;
    gap: 12px !important;
}

.gr-gallery .thumbnail-item {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    transition: all 0.3s ease !important;
}

.gr-gallery .thumbnail-item:hover {
    transform: scale(1.05) !important;
    border-color: var(--accent-primary) !important;
    box-shadow: var(--accent-glow) !important;
}

/* ===== LABELS ===== */
label, .gr-label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* Info text under inputs */
.gr-info, .gr-form .info {
    color: var(--text-muted) !important;
    font-size: 12px !important;
}

/* ===== DROPDOWN ===== */
.gr-dropdown {
    background: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
}

.gr-dropdown:focus-within {
    border-color: var(--accent-primary) !important;
    box-shadow: var(--accent-glow) !important;
}

/* ===== CHECKBOX ===== */
.gr-checkbox input[type="checkbox"] {
    accent-color: var(--accent-primary) !important;
    width: 18px !important;
    height: 18px !important;
}

/* ===== TEXTBOX (status) ===== */
.gr-textbox textarea[readonly], .gr-textbox.readonly textarea {
    background: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid var(--border-glass) !important;
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 13px !important;
}

/* ===== PROGRESS BAR ===== */
.progress-bar {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

.progress-bar .progress {
    background: var(--accent-gradient) !important;
    box-shadow: var(--accent-glow) !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--accent-primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-secondary);
}

/* ===== ANIMATIONS ===== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); }
    50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.5); }
}

.gr-panel {
    animation: fadeIn 0.5s ease-out;
}

/* ===== HEADINGS ===== */
h1, h2, h3, h4 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

h3 {
    font-size: 16px !important;
    margin-bottom: 12px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

/* ===== DIVIDERS ===== */
hr {
    border: none !important;
    height: 1px !important;
    background: var(--border-glass) !important;
    margin: 20px 0 !important;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .gr-button.primary {
        width: 100% !important;
    }
    
    .tab-nav {
        flex-wrap: wrap !important;
    }
    
    .tab-nav button {
        flex: 1 1 auto !important;
        min-width: 100px !important;
    }
}

/* ===== HOVER EFFECTS FOR CARDS ===== */
.gr-panel:hover {
    border-color: rgba(139, 92, 246, 0.3) !important;
}

/* ===== SPECIAL CLASSES ===== */
.glow-text {
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.glass-card {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-lg) !important;
    padding: 20px !important;
}

/* ===== STATUS INDICATORS ===== */
.status-success { color: var(--success) !important; }
.status-warning { color: var(--warning) !important; }
.status-error { color: var(--error) !important; }
"""
