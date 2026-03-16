import flet as ft

def dashboard_view(app_state):
    """Vista principal del Dashboard."""
    
    def metric_card(title, value_ctrl):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=12, color="#8b949e", weight="bold"),
                value_ctrl,
                ft.ProgressBar(width=200, color="#58a6ff", bgcolor="#30363d", value=0.1)
            ], spacing=10),
            padding=25, bgcolor="#161b22", border_radius=15, border=ft.border.all(1, "#30363d"), expand=True
        )

    # Creamos el botón dinámicamente para que sea reactivo
    app_state.zeus_master_btn = ft.Container(
        content=ft.Text(
            "⚡ MODO ZEUS: ACTIVO" if app_state.zeus_mode_on else "🛡️ MODO ZEUS: APAGADO", 
            color="white", 
            weight="bold"
        ),
        bgcolor="#238636" if app_state.zeus_mode_on else "#d73a49",
        padding=ft.padding.symmetric(vertical=15, horizontal=20),
        border_radius=8,
        on_click=app_state.optimize_action
    )

    return ft.Column([
        # Header
        ft.Row([
            ft.Column([
                ft.Text("Command Center Dashboard", size=34, weight="bold"),
                ft.Text("Vista general del rendimiento del sistema", color="#8b949e", size=15),
            ]),
            ft.Container(expand=True),
            app_state.zeus_master_btn
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

        ft.Container(height=30),

        # Stats Section
        ft.Row([
            metric_card("CPU PERFORMANCE", app_state.cpu_usage),
            metric_card("RAM STABILITY", app_state.ram_usage),
        ], spacing=25),

        ft.Container(height=30),

        # System Glance
        ft.Container(
            content=ft.Column([
                ft.Text("Estado del Zeus Shield", size=20, weight="bold"),
                ft.Container(height=10),
                ft.Row([
                    ft.Text("🛡️", size=18),
                    app_state.status_msg,
                ]),
                ft.Text("Detección de stutters activa. Modo de baja latencia habilitado.", color="#8b949e", size=13),
            ], spacing=10),
            padding=30, bgcolor="#161b22", border_radius=15, border=ft.border.all(1, "#30363d")
        ),
        
        ft.Container(expand=True),
    ], expand=True, spacing=0)
