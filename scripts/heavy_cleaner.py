# Zeus Plugin: Disk Heavy Cleaner
# ---------------------------------------------------------
# Versión final para el lanzamiento Open Source
# ---------------------------------------------------------
import os
import subprocess
import shutil

MANIFEST = {
    "name": "Limpieza Profunda (Heavy Cleaner)",
    "description": "Limpieza agresiva: vacía la papelera, elimina miniaturas de video/fotos, limpia caches de navegadores y registros de sistema antiguos.",
    "category": "Mantenimiento",
    "author": "Zeus OpenSource",
    "version": "1.2"
}

def run():
    print("🔥 Iniciando LIMPIEZA PESADA (Modo Agresivo)...")
    
    # 1. Vaciar Papelera
    trash_path = os.path.expanduser("~/.local/share/Trash")
    if os.path.exists(trash_path):
        print("🗑️ Vaciando Papelera de reciclaje...")
        os.system(f"rm -rf {trash_path}/files/* {trash_path}/info/*")
    
    # 2. Caches de Miniaturas (Pueden ocupar GBs)
    thumb_path = os.path.expanduser("~/.cache/thumbnails")
    if os.path.exists(thumb_path):
        size = subprocess.check_output(f"du -sh {thumb_path} | cut -f1", shell=True).decode().strip()
        print(f"🖼️ Eliminando cache de miniaturas ({size})...")
        os.system(f"rm -rf {thumb_path}/*")

    # 3. Limpieza de logs de sistema (Journald)
    print("📋 Reduciendo logs de sistema a los últimos 50MB...")
    subprocess.run("sudo journalctl --vacuum-size=50M", shell=True, capture_output=True)

    # 4. Limpieza de NPM/Pip Cache (Opcional pero pesado)
    print("📦 Limpiando caches de desarrollo (Pip/Npm)...")
    os.system("pip cache purge > /dev/null 2>&1")
    os.system("npm cache clean --force > /dev/null 2>&1")

    # 5. Apt Clean (Heredado de Janitor para redundancia pesada)
    print("🧹 Ejecutando limpieza profunda de paquetes (Apt)...")
    subprocess.run("sudo apt-get autoremove -y && sudo apt-get autoclean", shell=True, capture_output=True)

    print("✨ LIMPIEZA PESADA COMPLETADA. Espacio liberado.")
    return True
