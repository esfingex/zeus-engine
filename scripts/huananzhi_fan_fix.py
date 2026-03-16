# Zeus Plugin: Huananzhi Fan Fix (X99)
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import os
import subprocess

MANIFEST = {
    "name": "Huananzhi Fan Fix (X99)",
    "description": "Parche específico para corregir la velocidad de los ventiladores en placas base HUANANZHI. Solo aplicar si tienes una placa X99 china.",
    "category": "Hardware Fix",
    "author": "Iván Masías",
    "version": "1.0"
}

def run():
    print("🛠️ Verificando compatibilidad de Hardware...")
    
    try:
        with open("/sys/class/dmi/id/sys_vendor", "r") as f:
            vendor = f.read().strip()
    except:
        vendor = "Unknown"

    if "HUANANZHI" not in vendor.upper():
        print(f"⚠️ Hardware no compatible detectado ({vendor}).")
        print("❌ Este parche solo es para placas HUANANZHI.")
        return False

    print("✅ Placa HUANANZHI detectada. Aplicando parche de ventiladores...")
    
    # Buscamos el script original relativo a este plugin
    script_dir = os.path.dirname(os.path.abspath(__file__))
    legacy_path = os.path.join(script_dir, "easyway_for_ubuntu/install_huananzhi_fan_fix.sh")
    
    if os.path.exists(legacy_path):
        print("📦 Ejecutando parche heredado...")
        subprocess.run(f"sudo chmod +x {legacy_path}", shell=True)
        res = subprocess.run(f"sudo {legacy_path}", shell=True, capture_output=True, text=True)
        print(res.stdout)
        return res.returncode == 0
    else:
        print("❌ No se encontró el script original 'install_huananzhi_fan_fix.sh'.")
        print("💡 Asegúrate de que el repositorio easyway_for_ubuntu esté clonado.")
        return False
