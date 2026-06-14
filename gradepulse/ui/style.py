def inject_neumorphic_styles():
    ui.add_head_html('''
    <style>
        body {
            background: #e8edf2;
            color: #1a1a1a;
            font-family: 'Segoe UI', sans-serif;
        }
        .neu-card {
            background: #e8edf2;
            border-radius: 24px;
            box-shadow: 8px 8px 16px #cbd0d6, -8px -8px 16px #ffffff;
            padding: 24px;
            margin: 12px;
        }
        .neu-input {
            background: #e8edf2;
            border: none;
            border-radius: 16px;
            box-shadow: inset 4px 4px 8px #cbd0d6, inset -4px -4px 8px #ffffff;
            padding: 12px 16px;
            font-size: 1rem;
            width: 100%;
            outline: none;
            color: #1a1a1a;
        }
        .neu-btn {
            background: #e8edf2;
            border: none;
            border-radius: 16px;
            box-shadow: 5px 5px 12px #cbd0d6, -5px -5px 12px #ffffff;
            padding: 12px 28px;
            font-weight: 600;
            color: #1a1a1a;
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .neu-btn:active {
            box-shadow: inset 5px 5px 12px #cbd0d6, inset -5px -5px 12px #ffffff;
        }
        .neu-btn:hover {
            filter: brightness(0.98);
        }
        .dark-mode body {
            background: #2a2d32;
            color: #f0f0f0;
        }
        .dark-mode .neu-card {
            background: #2a2d32;
            box-shadow: 8px 8px 16px #1a1c1e, -8px -8px 16px #3a3e44;
            color: #f0f0f0;
        }
        .dark-mode .neu-input {
            background: #2a2d32;
            box-shadow: inset 4px 4px 8px #1a1c1e, inset -4px -4px 8px #3a3e44;
            color: #f0f0f0;
        }
        .dark-mode .neu-btn {
            background: #2a2d32;
            box-shadow: 5px 5px 12px #1a1c1e, -5px -5px 12px #3a3e44;
            color: #f0f0f0;
        }
        .dark-mode .neu-btn:active {
            box-shadow: inset 5px 5px 12px #1a1c1e, inset -5px -5px 12px #3a3e44;
        }
    </style>
    ''')