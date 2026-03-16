# Zeus Plugin: System Bloatware Cleaner
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess

MANIFEST = {
    "name": "Limpiador de Bloatware (Ubuntu)",
    "description": "Elimina aplicaciones pre-instaladas que consumen espacio y recursos: LibreOffice, Transmission, Remmina y Thunderbird.",
    "category": "Mantenimiento",
    "author": "Iván Masías",
    "version": "1.0"
}

def run():
    print("🧹 Iniciando limpieza de Bloatware...")
    
    # Lista de paquetes a purgar
    bloatware = [
        "libreoffice-*",
        "transmission-*",
        "remmina",
        "thunderbird"
    ]
    
    for app in bloatware:
        print(f"🗑️ Eliminando {app}...")
        subprocess.run(f"sudo apt-get purge {app} -y", shell=True, capture_output=True)
    
    print("📦 Limpiando dependencias huerfanas...")
    subprocess.run("sudo apt-get autoremove -y", shell=True, capture_output=True)
    
    print("✨ Limpieza de bloatware completada.")
    return True
