# Zeus Plugin: Nvidia Driver Status & Optimizer
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess
import shutil

MANIFEST = {
    "name": "Nvidia Driver & Performance",
    "description": "Verifica drivers Nvidia y configura el PPA de Graphics Drivers para máximo rendimiento.",
    "category": "Mantenimiento",
    "author": "Iván Masías",
    "version": "1.2"
}

def run():
    print("🎮 Verificando subsistema Gráfico...")
    
    # 1. Comprobar si hay GPU Nvidia
    res_lspci = subprocess.run("lspci | grep -i nvidia", shell=True, capture_output=True, text=True)
    if not res_lspci.stdout:
        print("ℹ️ No se detectó ninguna GPU Nvidia activa.")
        return True

    print("✅ GPU Nvidia encontrada.")
    
    # 2. Comprobar driver instalado
    if shutil.which("nvidia-smi"):
        try:
            res_smi = subprocess.check_output("nvidia-smi --query-gpu=driver_version --format=csv,noheader", shell=True).decode().strip()
            print(f"🚀 Driver detectado: v{res_smi}")
        except:
            print("⚠️ nvidia-smi falló. ¿Está el driver bien instalado?")
    else:
        print("❌ Driver de Nvidia NO encontrado.")
        print("💡 Se recomienda instalar via 'Software & Updates'.")

    # 3. Comprobar/Instalar PPA
    print("📂 Verificando PPA de Graphics Drivers...")
    res_ppa = subprocess.run("ls /etc/apt/sources.list.d | grep graphics-drivers", shell=True, capture_output=True, text=True)
    if res_ppa.stdout:
        print("✅ PPA 'graphics-drivers' ya está activo.")
    else:
        print("ℹ️ PPA 'graphics-drivers' no detectado.")
        # Podríamos instalarlo aquí, pero es mejor que sea informativo o pregunte
        print("💡 Sugerencia: Para drivers más nuevos, usa: sudo add-apt-repository ppa:graphics-drivers/ppa")

    return True
