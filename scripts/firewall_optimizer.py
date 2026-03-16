# Zeus Plugin: Firewall Optimizer
# ---------------------------------------------------------
# Ported from legacy custom_ubuntu.sh by Iván Masías
# ---------------------------------------------------------
import subprocess

MANIFEST = {
    "name": "Firewall Gamer (Seguridad)",
    "description": "Configura UFW para denegar todo el tráfico entrante de red y permitir solo el saliente. Máxima seguridad minimizando lag por escaneos externos.",
    "category": "Seguridad",
    "author": "Iván Masías",
    "version": "1.0"
}

def run():
    print("🛡️ Configurando reglas de Firewall Zeus...")
    
    tasks = [
        ("ufw default deny incoming", "Denegando entrante"),
        ("ufw default allow outgoing", "Permitiendo saliente"),
        ("ufw enable", "Activando Firewall")
    ]
    
    success = True
    for cmd, desc in tasks:
        print(f"📡 {desc}...")
        res = subprocess.run(f"sudo {cmd} --force", shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  ⚠️ Error en {cmd}: {res.stderr}")
            success = False
            
    if success:
        print("✅ Firewall configurado y activo.")
    return success
