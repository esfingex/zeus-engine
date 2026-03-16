# Zeus Plugin: Liquorix Kernel Installer
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess
import shutil

MANIFEST = {
    "name": "Kernel Liquorix (Gaming)",
    "description": "Kernel de alto rendimiento diseñado para gaming y bajas latencias. Ideal para eliminar micro-stutters.",
    "category": "Kernel/Power",
    "author": "Iván Masías",
    "version": "1.1"
}

def run():
    print("🚀 Iniciando instalación de Liquorix Kernel...")
    
    # Verificamos si ya tenemos un kernel con nombre liquorix
    try:
        current_kernel = subprocess.check_output("uname -r", shell=True).decode().lower()
        if "liquorix" in current_kernel:
            print("✅ El sistema ya está arrancado con el Kernel Liquorix.")
            return True
    except:
        pass

    if not shutil.which("curl"):
        print("📦 Instalando curl para descargar el script...")
        subprocess.run("sudo apt-get install -y curl", shell=True, capture_output=True)

    print("📡 Descargando y ejecutando instalador oficial de liquorix.net...")
    cmd = "curl -s 'https://liquorix.net/install-liquorix.sh' | sudo bash"
    
    try:
        # Ejecutamos con shell=True porque hay un pipe
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Instalación completada con éxito.")
            print("🔄 IMPORTANTE: Reinicia tu equipo para arrancar con el nuevo kernel.")
            return True
        else:
            print("❌ Error durante la instalación.")
            if result.stderr:
                print(f"  > {result.stderr.strip()[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Error crítico de red o ejecución: {str(e)}")
        return False
