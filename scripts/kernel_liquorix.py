# Zeus Plugin: Liquorix Kernel Installer
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import os
import subprocess

MANIFEST = {
    "name": "Kernel Liquorix (Gaming)",
    "description": "Kernel de alto rendimiento diseñado para gaming y bajas latencias. Ideal para eliminar micro-stutters.",
    "category": "Kernel/Power",
    "author": "Iván Masías",
    "version": "1.0"
}

def run():
    print("🚀 Iniciando instalación de Liquorix Kernel...")
    print("📦 Agregando repositorio oficial...")
    
    # Usamos curl para la instalación directa recomendada por liquorix.net
    cmd = "curl -s 'https://liquorix.net/install-liquorix.sh' | sudo bash"
    
    try:
        # Ejecutamos con shell=True porque hay un pipe
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Instalación completada con éxito.")
            print("🔄 IMPORTANTE: Reinicia tu equipo para arrancar con el nuevo kernel.")
            return True
        else:
            print(f"❌ Error durante la instalación: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        return False
