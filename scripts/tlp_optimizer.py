# Zeus Plugin: TLP Power Manager
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess
import shutil

MANIFEST = {
    "name": "Gestor de Energía TLP",
    "description": "Instala y activa TLP para una gestión inteligente de energía. Optimiza el consumo y la estabilidad térmica.",
    "category": "Kernel/Power",
    "author": "Iván Masías",
    "version": "1.1"
}

def run():
    print("🔋 Configurando Gestor de Energía TLP...")
    
    if not shutil.which("tlp"):
        print("📦 TLP no detectado. Agregando repositorio PPA...")
        try:
            subprocess.run("sudo add-apt-repository ppa:linrunner/tlp -y", shell=True, capture_output=True)
            subprocess.run("sudo apt-get update", shell=True, capture_output=True)
            print("📦 Instalando paquetes tlp y tlp-rdw...")
            res = subprocess.run("sudo apt-get install -y tlp tlp-rdw", shell=True, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"  ⚠️ Fallo en instalación de TLP: {res.stderr[:100]}")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    print("⚙️ Activando y arrancando servicio TLP...")
    try:
        subprocess.run("sudo systemctl enable tlp --now", shell=True, capture_output=True)
        subprocess.run("sudo tlp start", shell=True, capture_output=True)
        
        # Verificamos estado
        res_stat = subprocess.run("tlp-stat -s", shell=True, capture_output=True, text=True)
        if "enabled" in res_stat.stdout.lower():
            print("✅ TLP configurado, habilitado y en ejecución.")
        else:
            print("ℹ️ TLP instalado pero requiere reinicio para reporte de estado completo.")
    except Exception as e:
        print(f"  ⚠️ Error al iniciar servicio: {e}")
    
    return True
