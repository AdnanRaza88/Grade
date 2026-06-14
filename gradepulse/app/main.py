from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()

from ui.pages import dashboard, upload, config, results, ai, notebooklm

@ui.page('/')
def serve_dashboard():
    dashboard.render()

@ui.page('/upload')
def serve_upload():
    upload.render()

@ui.page('/config')
def serve_config():
    config.render()

@ui.page('/results')
def serve_results():
    results.render()

@ui.page('/ai')
def serve_ai():
    ai.render()

@ui.page('/notebooklm')
def serve_notebooklm():
    notebooklm.render()

nicegui_app.mount(app, '/api')