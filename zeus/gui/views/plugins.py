import flet as ft
import os
import traceback

def plugins_view(app_state):
    """Vista de Plugins con máxima compatibilidad y manejo de errores."""
    
    try:
        # Descubrimos plugins
        plugins = app_state.plugin_manager.discover_plugins()

        def plugin_card(info):
            # Usamos get() por si acaso faltan llaves
            name = info.get("name", "Desconocido")
            desc = info.get("description", "Sin descripción")
            cat = str(info.get("category", "General")).upper()
            file_name = info.get("file", "??")
            
            # Construcción manual hiper-compatible
            return ft.Container(
                content=ft.Row([
                    ft.Text("🐍", size=24),
                    ft.Column([
                        ft.Row([
                            ft.Text(name, size=16, weight="bold"),
                            ft.Text(f"[{cat}]", size=10, color="#58a6ff"),
                        ], spacing=10),
                        ft.Text(desc, color="#8b949e", size=12),
                        ft.Text(f"Archivo: {file_name}", color="#484f58", size=10, italic=True),
                    ], expand=True),
                    ft.ElevatedButton(
                        "EJECUTAR",
                        bgcolor="#238636",
                        color="white",
                        on_click=lambda _: app_state.run_external_script(file_name)
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=15,
                bgcolor="#161b22",
                border_radius=10,
                border=ft.border.all(1, "#30363d")
            )

        # Header con botón de refresco hiper-compatible (usando ElevatedButton en lugar de IconButton/Container)
        header = ft.Row([
            ft.Column([
                ft.Text("Scripts y Extensiones", size=30, weight="bold"),
                ft.Text("Librería modular en Python", color="#8b949e", size=14),
            ], expand=True),
            ft.ElevatedButton(
                "RECARGAR",
                icon="refresh", # Probamos string literal directamente
                on_click=app_state.refresh_plugins,
                bgcolor="#21262d",
                color="#58a6ff"
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Lista de contenido
        content_items = []
        if plugins:
            for p in plugins:
                try:
                    content_items.append(plugin_card(p))
                except Exception as e:
                    content_items.append(ft.Text(f"⚠️ Error en tarjeta: {e}", color="red"))
        else:
            content_items.append(ft.Text("No se detectaron scripts en /scripts", color="#ff7b72"))

        return ft.Column([
            header,
            ft.Divider(height=30, color="#30363d"),
            ft.Column(content_items, spacing=15, scroll=ft.ScrollMode.AUTO, expand=True),
            ft.Container(height=10),
            ft.Text("💡 Los scripts se ejecutan de forma segura.", color="#484f58", size=11),
        ], expand=True, spacing=0)

    except Exception as e:
        # Si todo falla, mostramos el error crítico en pantalla en lugar de pantalla gris
        error_stack = traceback.format_exc()
        print(f"❌ CRASH en plugins_view: {error_stack}")
        return ft.Column([
            ft.Text("💥 Error crítico al cargar la vista de Plugins", size=20, color="red", weight="bold"),
            ft.Text(f"Detalle: {str(e)}", color="orange"),
            ft.Divider(),
            ft.Text(error_stack, size=10, color="#8b949e", font_family="monospace")
        ], scroll=ft.ScrollMode.AUTO)
