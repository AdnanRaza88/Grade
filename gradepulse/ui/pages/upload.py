from nicegui import ui
from ui.style import inject

def render():
    inject()
    dark = ui.dark_mode()
    with ui.header().classes('items-center justify-between'):
        ui.button(on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.space()
        ui.button(icon='dark_mode' if not dark.value else 'light_mode', on_click=dark.toggle).props('flat round')

    ui.label('Upload Grades').classes('text-h3 q-my-md')
    upload = ui.upload(on_upload=handle, max_file_size=10*1024*1024).props('accept=.csv,.xlsx').classes('neu-card')
    errors_container = ui.column().classes('w-3/4')

    def handle(e):
        content = e.content
        name = e.name
        ui.run_javascript(f'''
            const blob = new Blob([new Uint8Array({list(content)})]);
            const formData = new FormData();
            formData.append("file", blob, "{name}");
            fetch("/api/upload/validate", {{ method: "POST", body: formData }})
              .then(r => r.json())
              .then(data => {{
                  const errDiv = getElement({errors_container.id});
                  errDiv.innerHTML = "";
                  if (data.errors.length > 0) {{
                      data.errors.forEach(err => {{
                          let p = document.createElement("p");
                          p.innerText = "Row " + err.row + ": " + err.error;
                          errDiv.appendChild(p);
                      }});
                      return;
                  }}
                  fetch("/api/upload/insert", {{ method: "POST", body: formData }})
                    .then(r => r.json())
                    .then(d => {{
                        alert("Inserted " + d.inserted + " records");
                        window.location.href = "/";
                    }});
              }})
        ''')