# Zeus Plugin: Huananzhi Fan Fix (X99) - Native Python Edition
# ---------------------------------------------------------
# Ported from legacy install_huananzhi_fan_fix.sh by Iván Masías
# ---------------------------------------------------------
import os
import subprocess
import shutil

MANIFEST = {
    "name": "Huananzhi Fan Fix (Nativo)",
    "description": "Habilita el control de ventiladores en placas HUANANZHI X99 (Chip Nuvoton). Modifica GRUB y configura el módulo nct6775.",
    "category": "Hardware Fix",
    "author": "Iván Masías",
    "version": "2.0"
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

    print("✅ Placa HUANANZHI detectada. Iniciando port nativo del Fan Fix...")

    # 1. Instalar herramientas de sensores
    print("📦 Instalando lm-sensors y fancontrol...")
    subprocess.run("sudo apt-get install -y lm-sensors fancontrol", shell=True, capture_output=True)

    # 2. Añadir parámetro al GRUB
    print("📝 Verificando parámetros de GRUB...")
    grub_path = "/etc/default/grub"
    param = "acpi_enforce_resources=lax"
    
    try:
        with open(grub_path, "r") as f:
            content = f.read()
        
        if param not in content:
            print(f"➕ Añadiendo '{param}' al GRUB...")
            # Usamos una aproximación segura para insertar el parámetro
            new_content = ""
            for line in content.split("\n"):
                if line.startswith("GRUB_CMDLINE_LINUX_DEFAULT="):
                    if '"' in line:
                        parts = line.split('"')
                        # Insertar antes de las últimas comillas
                        line = f'{parts[0]}"{parts[1].strip()} {param} "{parts[2]}'
                    elif "'" in line:
                        parts = line.split("'")
                        line = f"{parts[0]}'{parts[1].strip()} {param} '{parts[2]}"
                new_content += line + "\n"
            
            with open("/tmp/grub_huananzhi", "w") as f:
                f.write(new_content)
            
            subprocess.run("sudo mv /tmp/grub_huananzhi /etc/default/grub", shell=True)
            print("🔄 Actualizando GRUB (update-grub)...")
            subprocess.run("sudo update-grub", shell=True, capture_output=True)
            print("✅ GRUB actualizado. REINICIO REQUERIDO.")
        else:
            print("✅ El parámetro de GRUB ya existe.")
    except Exception as e:
        print(f"❌ Error al modificar GRUB: {e}")

    # 3. Configurar carga del módulo nct6775
    print("⚙️ Configurando carga automática del módulo nct6775...")
    
    conf_load = "/etc/modules-load.d/huananzhi-fan.conf"
    conf_opts = "/etc/modprobe.d/huananzhi-fan.conf"
    
    try:
        # Carga del módulo
        subprocess.run(f"echo 'nct6775' | sudo tee {conf_load}", shell=True, capture_output=True)
        # Opciones del módulo (usando 0xd420 como en el script original de easyway)
        subprocess.run(f"echo 'options nct6775 force_id=0xd420' | sudo tee {conf_opts}", shell=True, capture_output=True)
        print("✅ Módulos configurados.")
    except Exception as e:
        print(f"❌ Error al configurar módulos: {e}")

    print("\n--- ✨ PROCESO COMPLETADO ---")
    print("🚀 Por favor, REINICIA el sistema para aplicar los cambios.")
    print("💡 Después del reinicio, podrás configurar tus curvas con 'sudo pwmconfig'.")
    
    return True
