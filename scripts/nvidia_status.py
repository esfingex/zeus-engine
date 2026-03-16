# Zeus Plugin: Nvidia Driver Status
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess
import shutil

MANIFEST = {
    "name": "Nvidia Driver & Performance",
    "description": "Verifica el estado de tus controladores Nvidia y comprueba si el PPA de Graphics Drivers esta configurado para el maximo rendimiento en juegos.",
    "category": "Mantenimiento",
    "author": "Iván Masías",
    "version": "1.0"
}

def run():
    print("🎮 Verificando subsistema Gráfico...")
    
    # 1. Comprobar si hay GPU Nvidia
    res_lspci = subprocess.run("lspci | grep -i nvidia", shell=True, capture_output=True, text=True)
    if not res_lspci.stdout:
        print("ℹ️ No se detectó ninguna GPU Nvidia activa.")
        return True

    print("✅ GPU Nvidia detectada.")
    
    # 2. Comprobar driver instalado
    if shutil.which("nvidia-smi"):
        print("🚀 nvidia-smi detectado:")
        res_smi = subprocess.run("nvidia-smi --query-gpu=driver_version --format=csv,noheader", shell=True, capture_output=True, text=True)
        print(f"  Versión Driver: {res_smi.stdout.strip()}")
    else:
        print("⚠️ Driver de Nvidia NO encontrado o mal configurado.")
        print("💡 Se recomienda instalar via 'Software & Updates' o usar el PPA de Graphics Drivers.")

    # 3. Comprobar PPA
    print("📂 Verificando PPA de Graphics Drivers...")
    res_ppa = subprocess.run("ls /etc/apt/sources.list.d | grep graphics-drivers", shell=True, capture_output=True, text=True)
    if res_ppa.stdout:
        print("✅ PPA 'graphics-drivers' ya está en el sistema.")
    else:
        print("ℹ️ PPA 'graphics-drivers' no detectado. Útil para versiones de drivers más nuevas.")

    return True
