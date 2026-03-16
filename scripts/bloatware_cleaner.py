# Zeus Plugin: System Bloatware Cleaner
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# Refined for stability and informative logging
# ---------------------------------------------------------
import subprocess

MANIFEST = {
    "name": "Limpiador de Bloatware (Ubuntu)",
    "description": "Elimina aplicaciones pre-instaladas que consumen espacio y recursos: LibreOffice, Transmission, Remmina y Thunderbird.",
    "category": "Mantenimiento",
    "author": "Iván Masías",
    "version": "1.1"
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
        print(f"🗑️ Verificando y eliminando {app}...")
        try:
            # Usamos apt-get purge con redirección para no saturar el log de Zeus si no es necesario
            res = subprocess.run(f"sudo apt-get purge {app} -y", shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  ✅ {app} eliminado satisfactoriamente.")
            else:
                # Si falla suele ser porque no está instalado, lo cual es un "éxito" para nosotros
                print(f"  ℹ️ {app} no encontrado o ya eliminado.")
        except Exception as e:
            print(f"  ❌ Error inesperado con {app}: {e}")
    
    print("📦 Consolidando base de datos de paquetes (autoremove/autoclean)...")
    subprocess.run("sudo apt-get autoremove -y && sudo apt-get autoclean", shell=True, capture_output=True)
    
    print("✨ Limpieza de bloatware completada.")
    return True
