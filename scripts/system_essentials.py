# Zeus Plugin: System Essentials (Ubuntu 24.04+ Edition)
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# Refined for modern Ubuntu versions (removing redundant tools)
# ---------------------------------------------------------
import subprocess
import shutil

MANIFEST = {
    "name": "Componentes de Sistema (Modernos)",
    "description": "Instala PRELOAD para acelerar el inicio de aplicaciones y limpia el cache de paquetes de forma agresiva para liberar espacio.",
    "category": "Rendimiento/Herramientas",
    "author": "Iván Masías",
    "version": "1.2"
}

def run():
    print("🚀 Optimizando aceleradores de sistema para Ubuntu 24.04+...")
    
    # Preload sigue siendo muy útil para predecir el lanzamiento de apps
    if not shutil.which("preload"):
        print("📦 Instalando Preload (Aprendizaje de uso de apps)...")
        subprocess.run("sudo apt-get update", shell=True)
        subprocess.run("sudo apt-get install -y preload", shell=True)
    else:
        print("✅ preload ya está instalado y activo.")

    # En 24.04, apt ya es suficientemente rápido. 
    # Añadimos limpieza de cache como compensación.
    print("🧹 Realizando limpieza profunda de paquetes (autoremove/autoclean)...")
    subprocess.run("sudo apt-get autoremove -y", shell=True)
    subprocess.run("sudo apt-get autoclean", shell=True)
        
    print("✨ Sistema optimizado con herramientas modernas.")
    return True
