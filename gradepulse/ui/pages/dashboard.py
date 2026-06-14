from nicegui import ui
from ui.style import inject

def render():
    inject()
    dark = ui.dark_mode()

    with ui.header().classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.image('/static/logo.jpg').classes('w-10 h-10 rounded-full')
            ui.label('GradePulse').classes('text-h5 q-ml-sm')
        ui.space()
        ui.button(icon='dark_mode' if not dark.value else 'light_mode', on_click=dark.toggle).props('flat round')

    with ui.left_drawer().classes('neu-card') as drawer:
        ui.label('GradePulse').classes('text-h4 q-mb-lg')
        ui.button('Dashboard', on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.button('Upload', on_click=lambda: ui.navigate.to('/upload')).props('flat')
        ui.button('Config', on_click=lambda: ui.navigate.to('/config')).props('flat')
        ui.button('Results', on_click=lambda: ui.navigate.to('/results')).props('flat')
        ui.button('AI Help', on_click=lambda: ui.navigate.to('/ai')).props('flat')
        ui.button('NotebookLM', on_click=lambda: ui.navigate.to('/notebooklm')).props('flat')
        ui.separator()
        ui.button('Export CSV', on_click=lambda: ui.download('/api/export/csv')).props('flat')
        ui.button('Export Excel', on_click=lambda: ui.download('/api/export/excel')).props('flat')
        ui.button('Export PDF', on_click=lambda: ui.download('/api/export/pdf')).props('flat')

    with ui.column().classes('w-full items-center'):
        ui.label('Dashboard').classes('text-h3 q-my-md')
        columns = [
            {'headerName': col, 'field': col, 'sortable': True}
            for col in ['id', 'student_name', 'subject', 'marks_obtained', 'total_marks', 'semester', 'date', 'exam_type']
        ]
        table = ui.aggrid({
            'columnDefs': columns,
            'rowData': [],
            'rowSelection': 'single',
        }).classes('w-4/5')
        ui.button('Refresh', on_click=lambda: fetch(table)).classes('neu-btn')

def fetch(table):
    ui.run_javascript(f'''
        fetch("/api/grades/")
          .then(r => r.json())
          .then(data => {{
              const grid = getElement({table.id});
              grid.options.rowData = data;
              grid.update();
          }})
    ''')