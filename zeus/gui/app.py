import flet as ft
from zeus.core.hardware import HardwareDetector
from zeus.core.runner import CommandRunner
from zeus.core.plugins import PluginManager
import os
import time
import threading
import psutil

# Importamos las vistas
from zeus.gui.views.dashboard import dashboard_view
from zeus.gui.views.optimization import optimization_view
from zeus.gui.views.hardware import hardware_view
from zeus.gui.views.settings import settings_view
from zeus.gui.views.plugins import plugins_view

class ZeusApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Zeus Engine - Command Center"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window_width = 1200
        self.page.window_height = 850
        self.page.bgcolor = "#0d1117"
        
        self.hw = HardwareDetector()
        self.runner = CommandRunner()
        
        # Path dinámico para scripts internos
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.plugin_manager = PluginManager(os.path.join(base_dir, "scripts"))
        
        # Shared UI State
        self.cpu_usage = ft.Text("0%", size=26, weight="bold", color="#58a6ff")
        self.ram_usage = ft.Text("0%", size=26, weight="bold", color="#58a6ff")
        self.cpu_bar = ft.ProgressBar(width=200, color="#58a6ff", bgcolor="#30363d", value=0)
        self.ram_bar = ft.ProgressBar(width=200, color="#3fb950", bgcolor="#30363d", value=0)
        self.status_msg = ft.Text("🟢 Zeus Shield Activo", size=14, color="#3fb950")
        self.zeus_mode_on = False
        self.zeus_master_btn = None # Referencia para el botón del dashboard
        
        # Navigation State
        self.main_content = ft.Container(expand=True)
        self.current_view = "dashboard"
        
        # Log System
        self.log_text = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, auto_scroll=True)
        
        self.setup_ui()
        self.navigate("dashboard")
        
        # Monitor Thread
        self.stop_monitor = False
        threading.Thread(target=self.update_stats, daemon=True).start()

    def update_stats(self):
        # Primer llamado a cpu_percent siempre devuelve 0.0, lo descartamos
        psutil.cpu_percent(interval=None)
        while not self.stop_monitor:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                self.cpu_usage.value = f"{cpu:.1f}%"
                self.ram_usage.value = f"{ram:.1f}%"
                self.cpu_bar.value = cpu / 100
                self.ram_bar.value = ram / 100
                # Color dinámico según carga
                self.cpu_bar.color = "#ff7b72" if cpu > 80 else ("#e3b341" if cpu > 50 else "#58a6ff")
                self.ram_bar.color = "#ff7b72" if ram > 80 else ("#e3b341" if ram > 50 else "#3fb950")
                self.page.update()
                time.sleep(1)
            except Exception:
                break

    def navigate(self, view_name):
        self.current_view = view_name
        self.page.clean()
        self.setup_ui()
        
        if view_name == "dashboard":
            self.main_content.content = dashboard_view(self)
        elif view_name == "optimization":
            self.main_content.content = optimization_view(self)
        elif view_name == "hardware":
            self.main_content.content = hardware_view(self)
        elif view_name == "settings":
            self.main_content.content = settings_view(self)
        elif view_name == "plugins":
            self.main_content.content = plugins_view(self)
            
        self.page.update()

    def refresh_plugins(self, e=None):
        self.add_log("Recargando lista de plugins (Python Only)...", "cmd")
        self.navigate("plugins") # Volver a navegar fuerza el refresco de la vista
        self.add_log("Lista de plugins actualizada.", "success")

    def sidebar_item(self, emoji, text, view_id):
        selected = (self.current_view == view_id)
        return ft.Container(
            content=ft.Row([
                ft.Text(emoji, size=18),
                ft.Text(text, color="white" if selected else "#8b949e", size=15, weight="bold" if selected else "normal")
            ], spacing=15),
            padding=ft.padding.symmetric(vertical=15, horizontal=25),
            border_radius=10,
            bgcolor="#21262d" if selected else None,
            on_click=lambda _: self.navigate(view_id),
            on_hover=self.on_btn_hover
        )

    def on_btn_hover(self, e):
        if e.control.bgcolor != "#21262d":
            e.control.bgcolor = "#1c2128" if e.data == "true" else None
            e.control.update()

    def add_log(self, text, type="info"):
        color = "#8b949e"
        if type == "success": color = "#3fb950"
        elif type == "error": color = "#ff7b72"
        elif type == "cmd": color = "#58a6ff"
        
        # También imprimimos en la terminal real para transparencia total
        print(f"[{type.upper()}] {text}")
        
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.controls.append(
            ft.Text(f"[{timestamp}] {text}", size=12, color=color, font_family="monospace")
        )
        if len(self.log_text.controls) > 100:
            self.log_text.controls.pop(0)
        self.page.update()

    def clear_logs(self):
        self.log_text.controls.clear()
        self.page.update()

    def run_opt_action(self, action_id):
        """Lanza la optimización en un hilo separado para no bloquear la UI."""
        self.add_log(f"Iniciando: {action_id}", "cmd")
        self.status_msg.value = f"⏳ Ejecutando {action_id}..."
        self.page.update()
        threading.Thread(target=self._exec_opt_action, args=(action_id,), daemon=True).start()

    def _exec_opt_action(self, action_id):
        try:
            res = self.runner.run_optimization(action_id)

            if "log" in res:
                for line in res["log"].split("\n"):
                    if line.strip():
                        self.add_log(line)

            if res["success"]:
                self.add_log(f"Éxito: {action_id}", "success")
                self.status_msg.value = f"✅ {action_id} completado"
                self.status_msg.color = "#3fb950"
            else:
                self.add_log(f"Fallo: {action_id}", "error")
                self.status_msg.value = "⚠️ Error. Revisa el log."
                self.status_msg.color = "#ff7b72"
        except Exception as e:
            self.add_log(f"Error crítico en {action_id}: {str(e)}", "error")
            self.status_msg.value = "⚠️ Error crítico."
            self.status_msg.color = "#ff7b72"

        self.page.update()

    def run_external_script(self, filename):
        self.add_log(f"Lanzando script externo: {filename}", "cmd")
        threading.Thread(target=self._exec_script, args=(filename,), daemon=True).start()

    def _exec_script(self, filename):
        try:
            res = self.plugin_manager.run_plugin(filename)
            
            if res.get("stdout"):
                for line in res["stdout"].split("\n"):
                    if line.strip(): self.add_log(f"  {line[:120]}")
            
            if res.get("stderr"):
                for line in res["stderr"].split("\n"):
                    if line.strip(): self.add_log(f"  ⚠️ {line[:120]}", "error")

            if res.get("success"):
                self.add_log(f"Script {filename} finalizado con éxito.", "success")
            else:
                self.add_log(f"Script {filename} terminó con error.", "error")
                
        except Exception as e:
            self.add_log(f"Fallo crítico al ejecutar script: {str(e)}", "error")

    def authorize_sudo(self, e):
        self.add_log("Solicitando autorización de privilegios via GUI...", "cmd")
        success = self.runner.request_sudo_gui()
        if success:
            self.add_log("Autorización concedida. Privilegios de Zeus activos.", "success")
            self.status_msg.value = "🟢 Zeus Shield (Autorizado)"
            self.status_msg.color = "#3fb950"
        else:
            self.add_log("Autorización cancelada o fallida.", "error")
        self.page.update()

    def optimize_action(self, e):
        if not self.zeus_mode_on:
            self.run_opt_action("Master Combo")
            self.zeus_mode_on = True
            if self.zeus_master_btn:
                self.zeus_master_btn.content.value = "⚡ MODO ZEUS: ACTIVO"
                self.zeus_master_btn.bgcolor = "#238636"
        else:
            self.run_opt_action("Revert Master")
            self.zeus_mode_on = False
            if self.zeus_master_btn:
                self.zeus_master_btn.content.value = "🛡️ MODO ZEUS: APAGADO"
                self.zeus_master_btn.bgcolor = "#d73a49"
        self.page.update()

    def setup_ui(self):
        # Sidebar
        sidebar = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text("⚡ ZEUS ENGINE", size=22, weight="bold", color="#58a6ff")
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    margin=ft.margin.only(bottom=30, top=10)
                ),
                self.sidebar_item("🏠", "Dashboard", "dashboard"),
                self.sidebar_item("🚀", "Optimización", "optimization"),
                self.sidebar_item("📜", "Scripts", "plugins"),
                self.sidebar_item("📟", "Hardware", "hardware"),
                self.sidebar_item("⚙️", "Ajustes", "settings"),
                ft.Container(height=30),
                ft.Text("IA POWER", size=11, color="#484f58", weight="bold", margin=ft.margin.only(left=20)),
                self.sidebar_item("🤖", "Advisor (🔒)", "advisor"),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Column([
                        ft.Text("PRIVILEGIOS", size=10, color="#484f58", weight="bold"),
                        ft.ElevatedButton(
                            "🔑 AUTORIZAR ZEUS",
                            on_click=self.authorize_sudo,
                            bgcolor="#238636",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=10),
                            width=220
                        )
                    ], spacing=5),
                    padding=ft.padding.only(left=20, right=20)
                ),
                ft.Container(expand=True),
                ft.Row([
                    ft.Text("Zeus v1.0", size=11, color="#484f58")
                ], alignment=ft.MainAxisAlignment.CENTER, margin=ft.margin.only(bottom=20))
            ]),
            width=260,
            bgcolor="#161b22",
            padding=ft.padding.only(top=30, bottom=10),
        )

        self.page.add(
            ft.Row([
                sidebar,
                ft.Container(
                    content=self.main_content,
                    padding=40,
                    expand=True
                )
            ], expand=True, spacing=0)
        )

def main(page: ft.Page):
    ZeusApp(page)

if __name__ == "__main__":
    ft.run(main)
