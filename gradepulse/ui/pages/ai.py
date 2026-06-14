from nicegui import ui
from ui.style import inject
import requests

def render():
    inject()
    ui.label('AI Assistant').classes('text-h3 q-my-md')
    questions = {
        1: 'Improve study habits',
        2: 'Revision techniques',
        3: 'Time management',
        4: 'Stay motivated',
        5: 'Study schedule'
    }
    q_select = ui.select(questions, label='Question', value=1).classes('neu-input w-1/3')
    grade_id = ui.number('Grade ID', value=1).classes('neu-input w-1/3')
    tip_output = ui.label().classes('neu-card q-pa-md')

    def get_tip():
        qid = q_select.value
        gid = grade_id.value
        resp = requests.post(f"/api/grades/{gid}/study-tips?question_id={qid}")
        if resp.status_code == 200:
            tip_output.set_text(resp.json()['tip'])
        else:
            tip_output.set_text('Error fetching tip.')

    health_output = ui.label().classes('neu-card q-pa-md')

    def get_health():
        resp = requests.post("/api/ai/health-tips")
        health_output.set_text(resp.json()['tip'])

    with ui.row():
        ui.button('Get Study Tip', on_click=get_tip).classes('neu-btn')
        ui.button('Health Tip', on_click=get_health).classes('neu-btn')