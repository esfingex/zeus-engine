import flet as ft
from zeus.gui.app import main as zeus_gui_main
import sys
import os

def main():
    # Aseguramos que no estamos en sudo
    if os.getuid() == 0:
        print("❌ Error: Zeus Engine no debe ejecutarse con privilegios de root.")
        sys.exit(1)
        
    # Flet 0.82+ prefiere ft.run() para evitar el DeprecationWarning de ft.app()
    ft.run(zeus_gui_main)

if __name__ == "__main__":
    main()
