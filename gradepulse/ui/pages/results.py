from nicegui import ui
from ui.style import inject
import requests

def render():
    inject()
    ui.label('Results').classes('text-h3 q-my-md')
    name_input = ui.input('Student Name').classes('neu-input w-1/3')
    result_area = ui.column().classes('w-3/4')

    def search():
        name = name_input.value
        if not name:
            return
        resp = requests.get(f"/api/results/{name}")
        result_area.clear()
        if resp.status_code == 404:
            with result_area:
                ui.label("Student not found").classes('text-negative')
            return
        data = resp.json()
        with result_area:
            ui.label(f"Overall: {data['overall_percentage']}%").classes('text-h5')
            cols = ['subject', 'marks_obtained', 'total_marks', 'semester', 'exam_type']
            rows = [{c: r[c] for c in cols} for r in data['records']]
            ui.aggrid({
                'columnDefs': [{'headerName': c, 'field': c} for c in cols],
                'rowData': rows,
            }).classes('w-full')

    def summary():
        resp = requests.get("/api/results/")
        data = resp.json()
        result_area.clear()
        with result_area:
            ui.label(f"Students: {data['total_students']}  |  Avg %: {data['avg_percentage']}%  |  Records: {data['total_records']}  |  Top: {data['highest_scorer']}").classes('text-body1')

    with ui.row():
        ui.button('Search', on_click=search).classes('neu-btn')
        ui.button('Summary', on_click=summary).classes('neu-btn')