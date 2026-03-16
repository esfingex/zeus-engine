import flet as ft

def optimization_view(app_state):
    """Vista de optimización UNIVERSAL adaptativa."""
    
    statuses = app_state.runner.get_optimization_statuses()
    is_x99 = app_state.hw.is_x99()
    
    def opt_card(emoji, title, desc, action_label, action_id, special_color=None):
        status = statuses.get(title, "INACTIVO")
        is_active = any(k in status.upper() for k in ["ACTIVO", "MÁXIMO", "PERFORMANCE", "APLICADO", "DETECCIÓN", "✅"])
        needs_reboot = "REINICIO" in status.upper()
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(emoji, size=24), 
                    ft.Text(title, size=15, weight="bold", expand=True),
                    ft.Container(
                        content=ft.Text(status, size=9, weight="bold", color="white"),
                        bgcolor="#d73a49" if needs_reboot else ("#238636" if is_active else "#30363d"),
                        padding=ft.padding.symmetric(vertical=4, horizontal=10),
                        border_radius=20
                    )
                ]),
                ft.Text(desc, color="#8b949e", size=11, height=35),
                ft.Container(height=5),
                ft.ElevatedButton(
                    action_label,
                    bgcolor="#21262d",
                    color="white",
                    on_click=lambda _: app_state.run_opt_action(action_id),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ], spacing=5),
            padding=20,
            bgcolor="#161b22",
            border_radius=15,
            border=ft.border.all(1, "#30363d"),
            expand=True
        )

    return ft.Column([
        ft.Row([
            ft.Column([
                ft.Text("Zeus Universal Optimizer", size=30, weight="bold"),
                ft.Text("Detectando hardware y aplicando túneles de rendimiento", color="#8b949e", size=14),
            ]),
            ft.Container(
                content=ft.Text("MODO ADAPTATIVO: " + ("X99 🐉" if is_x99 else "ESTÁNDAR 💻"), weight="bold", size=12),
                padding=ft.padding.symmetric(horizontal=15, vertical=8),
                border_radius=10,
                bgcolor="#1c2128",
                border=ft.border.all(1, "#30363d")
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Divider(height=30, color="#30363d"),

        ft.Row([
            opt_card("🧹", "Limpieza Sistema", "Conserje Zeus: PageCache y logs temporales.", "Limpiar Ahora", "Limpieza"),
            opt_card("🔥", "CPU Governor", "Optimización de frecuencias para gaming.", "Perfil Performance", "CPU Performance"),
        ], spacing=20),

        ft.Container(height=15),

        ft.Row([
            opt_card("🛠️", "Ajuste Hardware", 
                     "Parche X99: Fix de sensores y kernel." if is_x99 else "Ajuste Genérico: Optimización de buses de hardware.", 
                     "Aplicar Ajuste", "Ajuste Hardware"),
            opt_card("🌀", "Control Térmico", "Gestión inteligente de curvas de ventilación.", "Sincronizar Fans", "Thermal Control"),
        ], spacing=20),

        ft.Container(height=15),

        ft.Row([
            opt_card("📡", "Network Optimization", "Baja latencia: Parámetros TCP universales.", "Fix Latencia", "Network Optimization"),
            opt_card("🎮", "GameMode", "Feral GameMode: Prioridad de procesos.", 
                     "Instalar" if "NO INSTALADO" in statuses["GameMode"].upper() else "Verificar", 
                     "Instalar GameMode" if "NO INSTALADO" in statuses["GameMode"].upper() else "GameMode"),
        ], spacing=20),

        ft.Container(height=25),
        
        # Log Area
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("📋 LOG NATIVO (UNIVERSAL)", size=11, color="#58a6ff", weight="bold"),
                    ft.Container(expand=True),
                    ft.IconButton(
                        content=ft.Icon(name="delete_outline", size=16),
                        on_click=lambda _: app_state.clear_logs()
                    )
                ]),
                ft.Divider(height=1, color="#30363d"),
                ft.Container(content=app_state.log_text, expand=True, padding=5)
            ], spacing=10),
            padding=20, bgcolor="#0d1117", border_radius=12, border=ft.border.all(1, "#21262d"), expand=True
        ),
        
        ft.Container(height=10),
    ], expand=True, spacing=0)
