from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Label
from textual.containers import Container, Horizontal, Vertical
from zeus.core.hardware import HardwareDetector

class ZeusDashboard(App):
    """Interfaz Premium para Zeus Engine."""
    
    CSS = """
    Screen {
        background: #0d1117;
    }
    Header {
        background: #161b22;
        color: #58a6ff;
        border-bottom: solid #30363d;
    }
    #sidebar {
        width: 35;
        background: #0d1117;
        border-right: tall #30363d;
        padding: 1;
    }
    #main-content {
        padding: 2;
    }
    .card {
        background: #161b22;
        border: tall #30363d;
        margin-bottom: 1;
        padding: 1;
        height: auto;
    }
    .neon-blue {
        color: #58a6ff;
        text-style: bold;
        content-align: center middle;
        margin-bottom: 2;
    }
    .label-header {
        color: #8b949e;
        text-style: italic;
        margin-top: 1;
    }
    Button {
        width: 100%;
        margin-top: 1;
        background: #21262d;
        border: solid #30363d;
        color: #c9d1d9;
    }
    Button:hover {
        background: #238636;
        color: white;
        text-style: bold;
    }
    #hw-info {
        height: 10;
        border: double #58a6ff;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("⚡ ZEUS ENGINE ⚡", classes="neon-blue")
                yield Label("MENÚ DE CONTROL", classes="label-header")
                yield Button("🚀 Optimizar CPU", id="opt-cpu")
                yield Button("🔍 Scan Sensores", id="opt-sensors")
                yield Button("🎮 Modo Gaming", id="opt-gaming")
                yield Label("CONFIGURACIÓN", classes="label-header")
                yield Button("⚙️ Ajustes Avanzados", id="settings")
            with Vertical(id="main-content"):
                yield Static(id="hw-info", classes="card")
                yield Static("REGISTRO DE ACTIVIDAD\n---------------------", id="logs", classes="card")
        yield Footer()

    def on_mount(self) -> None:
        hw = HardwareDetector()
        info = f"Sistema: {hw.get_distro()}\nGPU: {hw.get_gpu()}\nCPU: {hw.get_cpu_info()['processor']}"
        self.query_one("#hw-info").update(info)
        self.query_one("#logs").update("🚀 Zeus Engine iniciado. Listo para optimizar.")

if __name__ == "__main__":
    app = ZeusDashboard()
    app.run()
