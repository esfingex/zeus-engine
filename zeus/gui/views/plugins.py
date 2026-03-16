import flet as ft
import os

def plugins_view(app_state):
    """Vista de Plugins y Scripts adicionales (Python & Bash)."""
    
    # Descubrimos plugins usando el manager con soporte de Manifest
    plugins = app_state.plugin_manager.discover_plugins()

    def plugin_card(info):
        is_python = info["type"] == "python"
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text("🐍" if is_python else "📜", size=24),
                    padding=10,
                ),
                ft.Column([
                    ft.Row([
                        ft.Text(info["name"], size=16, weight="bold"),
                        ft.Container(
                            content=ft.Text(info["category"].upper(), size=9, weight="bold", color="#58a6ff"),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            border=ft.border.all(1, "#58a6ff"),
                            border_radius=5
                        )
                    ], spacing=10),
                    ft.Text(info["description"], color="#8b949e", size=12),
                    ft.Text(f"Archivo: {info['file']}", color="#484f58", size=10, italic=True),
                ], expand=True),
                ft.ElevatedButton(
                    "EJECUTAR",
                    bgcolor="#238636",
                    color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=lambda _: app_state.run_external_script(info["file"])
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            bgcolor="#161b22",
            border_radius=12,
            border=ft.border.all(1, "#30363d")
        )

    return ft.Column([
        ft.Row([
            ft.Column([
                ft.Text("Scripts y Extensiones", size=34, weight="bold"),
                ft.Text("Librería modular de optimización nativa en Python", color="#8b949e", size=15),
            ], expand=True),
            ft.IconButton(
                content=ft.Icon("autorenew", color="#58a6ff"),
                tooltip="Recargar Plugins",
                on_click=app_state.refresh_plugins
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(height=40, color="#30363d"),

        ft.Column([
            plugin_card(p) for p in plugins
        ] if plugins else [ft.Text("No se detectaron scripts adicionales en /scripts", color="#ff7b72")], 
        spacing=15, scroll=ft.ScrollMode.AUTO, expand=True),

        ft.Container(height=20),
        ft.Text("💡 Los scripts de Python se ejecutan de forma aislada y segura.", color="#484f58", size=11),
    ], expand=True, spacing=0)
