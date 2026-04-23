import os
import subprocess
import shutil
from zeus.core.optimizations import CPUManager, SystemJanitor, SensorPatch, ThermalManager, NetworkManager, ZeusCoreBase, MasterOptimizer
from zeus.core.hardware import HardwareDetector

class CommandRunner:
    """Orquestador universal de optimizaciones con soporte de privilegios."""
    
    def __init__(self):
        self.hw = HardwareDetector()

    def check_sudo(self):
        """Verifica si tenemos permisos de sudo activos."""
        try:
            res = subprocess.run("sudo -n true", shell=True, capture_output=True)
            return res.returncode == 0
        except:
            return False

    def request_sudo_gui(self):
        """Lanza un diálogo nativo de Linux (pkexec) para validar privilegios."""
        try:
            res = subprocess.run("pkexec true", shell=True, capture_output=True)
            return res.returncode == 0
        except:
            return False

    def get_optimization_statuses(self):
        """Consulta el estado real adaptativo del sistema."""
        statuses = {
            "Limpieza Sistema": "Listo",
            "GameMode": "Inactivo",
            "CPU Governor": "Balanceado",
            "Ajuste Hardware": "Pendiente",
            "Control Térmico": "Inactivo",
            "Network Optimization": "DEFAULT"
        }
        
        # CPU Governor
        try:
            if os.path.exists("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"):
                with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor") as f:
                    gov = f.read().strip().upper()
                    statuses["CPU Governor"] = gov
        except: pass

        # GameMode
        if shutil.which("gamemoded"):
            try:
                s, out, err = ZeusCoreBase.run_command("gamemoded -s")
                statuses["GameMode"] = "ACTIVO ✅" if "is active" in out else "INSTALADO"
            except: pass
        else:
            statuses["GameMode"] = "NO INSTALADO"
            
        # Hardware Patch
        is_x99 = self.hw.is_x99()
        if is_x99:
            statuses["Ajuste Hardware"] = "X99 DETECTADO"
            if os.path.exists("/etc/sensors.d/zeus_x99.conf"):
                try:
                    with open("/proc/cmdline", "r") as f:
                        if "nct6775.force_id=0xd42b" in f.read():
                            statuses["Ajuste Hardware"] = "OPTIMIZADO ✅"
                        else:
                            statuses["Ajuste Hardware"] = "REINICIO REQUERIDO 🔄"
                except: statuses["Ajuste Hardware"] = "APLICADO ✅"
        else:
            statuses["Ajuste Hardware"] = "ESTÁNDAR"

        # Thermal Control
        if os.path.exists("/etc/fancontrol"):
            try:
                s, out, err = ZeusCoreBase.run_command("systemctl is-active fancontrol")
                statuses["Control Térmico"] = "ACTIVO ✅" if out.strip() == "active" else "DETENIDO"
            except: pass

        # Network Optimization (TCP low latency)
        try:
            tcp_ll_path = "/proc/sys/net/ipv4/tcp_low_latency"
            if os.path.exists(tcp_ll_path):
                with open(tcp_ll_path) as f:
                    val = f.read().strip()
                    statuses["Network Optimization"] = "ACTIVO ✅" if val == "1" else "DEFAULT"
            tcp_fo_path = "/proc/sys/net/ipv4/tcp_fastopen"
            if os.path.exists(tcp_fo_path):
                with open(tcp_fo_path) as f:
                    fo_val = f.read().strip()
                    if fo_val == "3" and statuses["Network Optimization"] == "ACTIVO ✅":
                        statuses["Network Optimization"] = "OPTIMIZADO ✅"
        except Exception:
            pass

        return statuses

    def run_optimization(self, action):
        """Punto de entrada adaptativo."""
        
        if action == "Limpieza":
            success, log = SystemJanitor.deep_clean()
            return {"success": success, "log": log}
            
        elif action == "CPU Performance":
            success, log = CPUManager.set_performance()
            return {"success": success, "log": log}
            
        elif action == "Master Combo":
            success, log = MasterOptimizer.run_master_combo(is_x99=self.hw.is_x99())
            return {"success": success, "log": log}
            
        elif action == "Revert Master":
            success, log = MasterOptimizer.revert_master_combo()
            return {"success": success, "log": log}
            
        elif action == "Ajuste Hardware":
            success, log = SensorPatch.apply_best_fix(is_x99=self.hw.is_x99())
            return {"success": success, "log": log}
            
        elif action == "Thermal Control":
            success, log = ThermalManager.auto_configure()
            return {"success": success, "log": log}
            
        elif action == "GameMode":
            log = "🎮 Verificando estado de Feral GameMode...\n"
            s, out, err = ZeusCoreBase.run_command("gamemoded -s")
            log += out + "\n" + err
            return {"success": s, "log": log}
            
        elif action == "Instalar GameMode":
            log = "📦 Instalando GameMode (Apt)...\n"
            s, out, err = ZeusCoreBase.run_command("apt-get update && apt-get install -y gamemode")
            log += out + "\n" + err
            return {"success": s, "log": log}

        elif action == "Network Optimization":
            success, log = NetworkManager.set_low_latency()
            return {"success": success, "log": log}

        return {"success": False, "log": f"Acción '{action}' no reconocida."}
