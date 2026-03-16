# Zeus Plugin: Disk Heavy Cleaner
# ---------------------------------------------------------
# Versión Pulida - Zeus Engine Open Source
# ---------------------------------------------------------
import os
import subprocess
import shutil

MANIFEST = {
    "name": "Limpieza Profunda (Heavy Cleaner)",
    "description": "Limpieza agresiva: vacía la papelera, elimina miniaturas, limpia caches de dev y registros de sistema antiguos.",
    "category": "Mantenimiento",
    "author": "Zeus OpenSource",
    "version": "1.3"
}

def get_dir_size(path):
    try:
        if os.path.exists(path):
            output = subprocess.check_output(f"du -sh {path} | cut -f1", shell=True).decode().strip()
            return output
    except:
        pass
    return "0B"

def run():
    print("🔥 Iniciando LIMPIEZA PESADA (Modo Agresivo)...")
    
    # 1. Vaciar Papelera
    trash_path = os.path.expanduser("~/.local/share/Trash")
    if os.path.exists(trash_path):
        size = get_dir_size(trash_path)
        print(f"🗑️ Vaciando Papelera ({size})...")
        os.system(f"rm -rf {trash_path}/files/* {trash_path}/info/*")
    
    # 2. Caches de Miniaturas
    thumb_path = os.path.expanduser("~/.cache/thumbnails")
    if os.path.exists(thumb_path):
        size = get_dir_size(thumb_path)
        print(f"🖼️ Eliminando cache de miniaturas ({size})...")
        os.system(f"rm -rf {thumb_path}/*")

    # 3. Logs de sistema
    print("📋 Reduciendo logs de sistema (Journald) a 50MB...")
    subprocess.run("sudo journalctl --vacuum-size=50M", shell=True, capture_output=True)

    # 4. Caches de Desarrollo
    print("📦 Limpiando caches de desarrollo (Pip/Npm)...")
    subprocess.run("pip cache purge", shell=True, capture_output=True)
    subprocess.run("npm cache clean --force", shell=True, capture_output=True)

    # 5. Apt Clean
    print("🧹 Ejecutando limpieza profunda de paquetes (Apt)...")
    subprocess.run("sudo apt-get autoremove -y && sudo apt-get autoclean", shell=True, capture_output=True)

    print("✨ LIMPIEZA PESADA COMPLETADA. Sistema purificado.")
    return True
