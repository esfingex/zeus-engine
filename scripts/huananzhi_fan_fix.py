# Zeus Plugin: Huananzhi Fan Fix (X99) - Native Python Edition
# ---------------------------------------------------------
# Ported from legacy install_huananzhi_fan_fix.sh by Iván Masías
# Refined for safety and robust GRUB parsing
# ---------------------------------------------------------
import os
import subprocess
import shutil

MANIFEST = {
    "name": "Huananzhi Fan Fix (Nativo)",
    "description": "Habilita el control de ventiladores en placas HUANANZHI X99. Modifica GRUB y configura el módulo nct6775.",
    "category": "Hardware Fix",
    "author": "Iván Masías",
    "version": "2.1"
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

    print("✅ Placa HUANANZHI detectada. Iniciando optimización nativa...")

    # 1. Herramientas
    print("📦 Asegurando herramientas térmicas (lm-sensors/fancontrol)...")
    subprocess.run("sudo apt-get install -y lm-sensors fancontrol", shell=True, capture_output=True)

    # 2. GRUB
    print("📝 Revisando configuración de arranque (GRUB)...")
    grub_path = "/etc/default/grub"
    param = "acpi_enforce_resources=lax"
    
    if not os.path.exists(grub_path):
        print("❌ Error: No se encontró /etc/default/grub")
        return False

    try:
        with open(grub_path, "r") as f:
            content = f.read()
        
        if param not in content:
            print(f"➕ Agregando '{param}' al GRUB...")
            new_lines = []
            for line in content.splitlines():
                if line.startswith("GRUB_CMDLINE_LINUX_DEFAULT="):
                    if '"' in line:
                        line = line.replace('"', f' {param} "', 1) if param not in line else line
                        # Limpieza de espacios dobles
                        line = line.replace('  ', ' ')
                    elif "'" in line:
                        line = line.replace("'", f" {param} ", 1) if param not in line else line
                new_lines.append(line)
            
            with open("/tmp/grub_zeus", "w") as f:
                f.write("\n".join(new_lines))
            
            subprocess.run("sudo mv /tmp/grub_zeus /etc/default/grub", shell=True)
            print("🔄 Ejecutando update-grub...")
            subprocess.run("sudo update-grub", shell=True, capture_output=True)
            print("✅ GRUB actualizado. REINICIO REQUERIDO.")
        else:
            print("✅ El parámetro lax ya está presente en GRUB.")
    except Exception as e:
        print(f"❌ Error modificando GRUB: {e}")

    # 3. Kernel Modules
    print("⚙️ Configurando carga de módulo nct6775...")
    try:
        subprocess.run("echo 'nct6775' | sudo tee /etc/modules-load.d/zeus-fan.conf", shell=True, capture_output=True)
        subprocess.run("echo 'options nct6775 force_id=0xd42b' | sudo tee /etc/modprobe.d/zeus-fan.conf", shell=True, capture_output=True)
        print("✅ Configuración de módulos completada (ID: 0xd42b).")
    except Exception as e:
        print(f"❌ Error en módulos: {e}")

    print("\n--- ✨ PROCESO ZEUS COMPLETADO ---")
    print("🚀 REINICIA el sistema para que los ventiladores sean controlables.")
    return True
