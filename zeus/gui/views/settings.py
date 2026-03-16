import flet as ft

def settings_view(app_state):
    """Vista de Ajustes de la Aplicación."""
    
    return ft.Column([
        ft.Text("Ajustes de Zeus Engine", size=34, weight="bold"),
        ft.Text("Configuración de la interfaz y el entorno de la aplicación", color="#8b949e", size=15),
        ft.Divider(height=40, color="#30363d"),

        ft.Container(
            content=ft.Column([
                ft.Text("🛠️ Preferencias de la GUI", size=20, weight="bold", color="#58a6ff"),
                ft.Text("Estos ajustes afectan el comportamiento de la ventana y los controles visuales.", color="#8b949e", size=13),
                ft.Container(height=10),
                ft.Switch(label="Animaciones suaves (Beta)", value=True, active_color="#58a6ff"),
                ft.Switch(label="Refresco automático de estados (2s)", value=True, active_color="#58a6ff"),
                ft.Switch(label="Cerrar al ejecutar optimización", value=False, active_color="#58a6ff"),
            ]),
            padding=25, bgcolor="#161b22", border_radius=15, border=ft.border.all(1, "#30363d")
        ),

        ft.Container(height=25),

        ft.Container(
            content=ft.Column([
                ft.Text("🔧 Entorno del Motor", size=20, weight="bold", color="#3fb950"),
                ft.Text("Detalles sobre la ejecución interna de Zeus.", color="#8b949e", size=13),
                ft.Container(height=10),
                ft.Text("Versión: 1.0.0 Stable Build", color="white"),
                ft.Text("Path: " + os.getcwd(), color="#484f58", size=11),
                ft.Container(height=10),
                ft.ElevatedButton("Ver logs en terminal", icon="terminal", on_click=lambda _: print("Logs solicitados desde GUI")),
            ]),
            padding=25, bgcolor="#161b22", border_radius=15, border=ft.border.all(1, "#30363d")
        ),

        ft.Container(expand=True),
    ], expand=True, spacing=0)

import os # Fix for getcwd
