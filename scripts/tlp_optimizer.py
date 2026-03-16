# Zeus Plugin: TLP Power Manager
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess
import shutil

MANIFEST = {
    "name": "Gestor de Energía TLP",
    "description": "Instala y activa TLP para una gestión inteligente de energía. Optimiza el consumo en portátiles y la estabilidad en sobremesa.",
    "category": "Kernel/Power",
    "author": "Iván Masías",
    "version": "1.0"
}

def run():
    print("🔋 Configurando Gestor de Energía TLP...")
    
    if not shutil.which("tlp"):
        print("📦 Instalando TLP desde repositorio oficial...")
        subprocess.run("sudo add-apt-repository ppa:linrunner/tlp -y", shell=True, capture_output=True)
        subprocess.run("sudo apt-get update", shell=True, capture_output=True)
        subprocess.run("sudo apt-get install -y tlp tlp-rdw", shell=True, capture_output=True)
    
    print("⚙️ Activando servicio TLP...")
    subprocess.run("sudo systemctl enable tlp --now", shell=True, capture_output=True)
    subprocess.run("sudo tlp start", shell=True, capture_output=True)
    
    print("✅ TLP configurado y en ejecución.")
    return True
