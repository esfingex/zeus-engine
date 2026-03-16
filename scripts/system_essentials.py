# Zeus Plugin: System Essentials (Ubuntu 24.04+ Edition)
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess
import shutil

MANIFEST = {
    "name": "Componentes de Sistema (Modernos)",
    "description": "Instala PRELOAD para acelerar el inicio de aplicaciones y realiza mantenimiento de paquetes.",
    "category": "Rendimiento/Herramientas",
    "author": "Iván Masías",
    "version": "1.3"
}

def run():
    print("🚀 Optimizando aceleradores de sistema para Ubuntu 24.04+...")
    
    # Preload
    if not shutil.which("preload"):
        print("📦 Instalando Preload (Acelerador de Apps)...")
        try:
            # Usamos update para asegurar que el repo está fresco
            subprocess.run("sudo apt-get update", shell=True, capture_output=True)
            res = subprocess.run("sudo apt-get install -y preload", shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print("  ✅ Preload instalado y configurado.")
            else:
                print(f"  ⚠️ No se pudo instalar preload: {res.stderr}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    else:
        print("✅ preload ya está presente en el sistema.")

    # Mantenimiento Apt
    print("🧹 Ejecutando rutinas de mantenimiento Apt...")
    try:
        subprocess.run("sudo apt-get autoremove -y", shell=True, capture_output=True)
        subprocess.run("sudo apt-get autoclean", shell=True, capture_output=True)
        print("  ✅ Mantenimiento de paquetes completado.")
    except Exception as e:
        print(f"  ⚠️ Error de mantenimiento: {e}")
        
    print("✨ Sistema optimizado con herramientas Zeus.")
    return True
