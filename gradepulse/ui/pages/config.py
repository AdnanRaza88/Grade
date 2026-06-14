from nicegui import ui
from ui.style import inject
import requests, json

def render():
    inject()
    ui.label('Configuration').classes('text-h3 q-my-md')
    passing = ui.number('Passing %', value=33, min=0, max=100).classes('neu-input w-1/3')
    a_min = ui.number('A grade min %', value=80).classes('neu-input w-1/3')
    b_min = ui.number('B grade min %', value=65).classes('neu-input w-1/3')
    c_min = ui.number('C grade min %', value=50).classes('neu-input w-1/3')
    d_min = ui.number('D grade min %', value=33).classes('neu-input w-1/3')

    def save():
        config = {
            "passing_percentage": passing.value,
            "A_min": a_min.value,
            "B_min": b_min.value,
            "C_min": c_min.value,
            "D_min": d_min.value
        }
        requests.put("/api/config/", json={"value": json.dumps(config)})
        ui.notify("Saved", type='positive')
    ui.button('Save', on_click=save).classes('neu-btn q-mt-md')