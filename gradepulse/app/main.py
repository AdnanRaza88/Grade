from fastapi import FastAPI
from nicegui import ui, app as nicegui_app
from app.database import init_db
from app.routers import grades, upload, export, config, results, ai

app = FastAPI(title="GradePulse")
app.include_router(grades.router)
app.include_router(upload.router)
app.include_router(export.router)
app.include_router(config.router)
app.include_router(results.router)
app.include_router(ai.router)

init_db()

from ui.pages import dashboard, upload_page, config_page, results_page, ai_page, notebooklm_page

@ui.page('/')
def dashboard_ui():
    dashboard.render()

@ui.page('/upload')
def upload_ui():
    upload_page.render()

@ui.page('/config')
def config_ui():
    config_page.render()

@ui.page('/results')
def results_ui():
    results_page.render()

@ui.page('/ai')
def ai_ui():
    ai_page.render()

@ui.page('/notebooklm')
def notebooklm_ui():
    notebooklm_page.render()

nicegui_app.mount(app, '/api')