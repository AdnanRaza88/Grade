from nicegui import ui, run_javascript
from ui.style import inject

def render():
    inject()
    ui.label('Upload Grades').classes('text-h3 q-my-md')
    upload = ui.upload(on_upload=handle, max_file_size=10*1024*1024).props('accept=.csv,.xlsx').classes('neu-card')
    errors_container = ui.column().classes('w-3/4')

def handle(e):
    content = e.content
    name = e.name
    run_javascript(f'''
        const blob = new Blob([new Uint8Array({list(content)})]);
        const formData = new FormData();
        formData.append("file", blob, "{name}");
        fetch("/api/upload/validate", {{ method: "POST", body: formData }})
          .then(r => r.json())
          .then(data => {{
              const errDiv = getElement({id(errors_container)});
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
    '''
    )