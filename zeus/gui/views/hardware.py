import flet as ft
import os

def hardware_view(app_state):
    """Vista detallada de Hardware."""
    
    hw_info = app_state.hw
    cpu_info = hw_info.get_cpu_info()
    
    def hw_row(label, value):
        return ft.Container(
            content=ft.Row([
                ft.Text(label, width=150, color="#8b949e", weight="bold"),
                ft.Text(value, color="white", weight="bold", expand=True),
            ]),
            padding=ft.padding.symmetric(vertical=10),
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#21262d"))
        )

    return ft.Column([
        ft.Text("Monitor de Hardware", size=34, weight="bold"),
        ft.Text("Detalles técnicos de los componentes detectados", color="#8b949e", size=15),
        ft.Divider(height=40, color="#30363d"),

        ft.Container(
            content=ft.Column([
                ft.Text("Unidad de Procesamiento (CPU)", size=20, weight="bold", color="#58a6ff"),
                ft.Container(height=10),
                hw_row("Arquitectura", cpu_info.get('architecture', 'Unknown')),
                hw_row("Procesador", cpu_info.get('processor', 'Unknown')),
                hw_row("Núcleos", cpu_info.get('cores', 'Unknown')),
                hw_row("Familia / Modelo", f"{cpu_info.get('family', 'N/A')} / {cpu_info.get('model', 'N/A')}"),
                hw_row("Plataforma X99", "Detectada ✅" if hw_info.is_x99() else "No detectada ❌"),
            ]),
            padding=25, bgcolor="#161b22", border_radius=15, border=ft.border.all(1, "#30363d")
        ),

        ft.Container(height=25),

        ft.Container(
            content=ft.Column([
                ft.Text("Gráficos y Sistema (GPU/OS)", size=20, weight="bold", color="#3fb950"),
                ft.Container(height=10),
                hw_row("Tarjeta Gráfica", hw_info.get_gpu()),
                hw_row("Driver NVIDIA", hw_info.get_nvidia_version()) if hw_info.get_gpu() == "NVIDIA" else ft.Container(),
                hw_row("Distribución", hw_info.get_distro()),
                hw_row("Kernel", os.popen("uname -r").read().strip()),
            ]),
            padding=25, bgcolor="#161b22", border_radius=15, border=ft.border.all(1, "#30363d")
        ),

        ft.Container(expand=True),
    ], expand=True, spacing=0, scroll=ft.ScrollMode.AUTO)
