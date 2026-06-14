from nicegui import ui
from ui.style import inject

def render():
    inject()
    ui.label('NotebookLM').classes('text-h3 q-my-md')
    ui.label('Enhance your learning with Google NotebookLM, an AI research assistant.').classes('text-body1')
    ui.link('Open NotebookLM', 'https://notebooklm.google.com').classes('neu-btn q-mt-md')