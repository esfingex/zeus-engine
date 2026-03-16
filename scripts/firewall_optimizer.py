# Zeus Plugin: Firewall Optimizer
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess

MANIFEST = {
    "name": "Firewall Gamer (Seguridad)",
    "description": "Configura UFW para denegar tráfico entrante y permitir saliente. Máxima seguridad para gaming.",
    "category": "Seguridad",
    "author": "Iván Masías",
    "version": "1.1"
}

def run():
    print("🛡️ Configurando reglas de Firewall Zeus...")
    
    # Instalamos ufw si no está
    subprocess.run("sudo apt-get install -y ufw", shell=True, capture_output=True)
    
    tasks = [
        ("ufw default deny incoming", "Bloqueando tráfico entrante"),
        ("ufw default allow outgoing", "Permitiendo tráfico saliente"),
        ("ufw logging off", "Desactivando logs (Minimiza I/O disk)"),
        ("ufw --force enable", "Activando Firewall")
    ]
    
    success = True
    for cmd, desc in tasks:
        print(f"📡 {desc}...")
        res = subprocess.run(f"sudo {cmd}", shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  ⚠️ Error en comando '{cmd}': {res.stderr[:100]}")
            success = False
            
    if success:
        print("✅ Firewall configurado, optimizado y activo.")
        # Mostramos estado resumido
        status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True)
        print(f"  Estado actual: {status.stdout.splitlines()[0] if status.stdout else 'Activo'}")
        
    return success
