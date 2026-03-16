import os
import subprocess
import shutil

class ZeusCoreBase:
    """Clase base con utilidades de ejecución robustas."""
    @staticmethod
    def run_command(cmd):
        try:
            result = subprocess.run(f"sudo {cmd}", shell=True, capture_output=True, text=True, timeout=60)
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)

class BootManager(ZeusCoreBase):
    """Gestiona los parámetros del kernel y el cargador de arranque GRUB."""
    
    @staticmethod
    def apply_kernel_patch(param, description="Parche de kernel"):
        log = f"🚀 Verificando {description}: {param}...\n"
        grub_file = "/etc/default/grub"
        
        if not os.path.exists(grub_file):
            return False, log + "❌ No se encontró /etc/default/grub.\n"
            
        try:
            with open(grub_file, "r") as f:
                content = f.read()
            
            if param in content:
                return True, log + "✅ El parámetro ya está presente en GRUB.\n"
            
            log += "📝 Modificando configuración de arranque...\n"
            new_content = ""
            found_line = False
            for line in content.split("\n"):
                if line.startswith("GRUB_CMDLINE_LINUX_DEFAULT="):
                    found_line = True
                    current_params = line.split('"')[1]
                    new_line = f'GRUB_CMDLINE_LINUX_DEFAULT="{current_params} {param}"'
                    new_content += new_line + "\n"
                else:
                    new_content += line + "\n"
            
            if not found_line:
                return False, log + "❌ No se pudo encontrar la línea GRUB_CMDLINE_LINUX_DEFAULT.\n"

            with open("/tmp/grub_zeus", "w") as f:
                f.write(new_content)
            
            os.system(f"sudo mv /tmp/grub_zeus {grub_file}")
            success, out, err = ZeusCoreBase.run_command("update-grub")
            log += out + "\n" + err + "\n"
            if success:
                log += "✅ GRUB actualizado. REINICIO REQUERIDO.\n"
            return success, log
        except Exception as e:
            return False, log + f"❌ Error: {str(e)}\n"

class CPUManager(ZeusCoreBase):
    """Gestión avanzada y adaptativa para Intel/AMD."""
    
    @staticmethod
    def get_cpu_vendor():
        try:
            with open("/proc/cpuinfo", "r") as f:
                content = f.read()
                if "AuthenticAMD" in content: return "amd"
                if "GenuineIntel" in content: return "intel"
        except: pass
        return "generic"

    @staticmethod
    def set_performance():
        log = "🚀 Optimizando escalado de CPU (PERFORMANCE)...\n"
        vendor = CPUManager.get_cpu_vendor()
        
        epp_path = "/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference"
        if os.path.exists(epp_path):
            ZeusCoreBase.run_command("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference")

        if shutil.which("cpupower"):
            success, out, err = ZeusCoreBase.run_command("cpupower frequency-set -g performance")
            if vendor == "intel":
                ZeusCoreBase.run_command("echo 100 | sudo tee /sys/devices/system/cpu/intel_pstate/min_perf_pct")
            return success, log + f"✅ Governor configurado a PERFORMANCE ({vendor}).\n"
        else:
            cmd = "echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, log + "✅ Governor forzado a PERFORMANCE via sysfs.\n"

    @staticmethod
    def set_balanced():
        log = "🍃 Restaurando escalado de CPU (EQUILIBRADO)...\n"
        vendor = CPUManager.get_cpu_vendor()
        
        # EPP a balance_performance
        epp_path = "/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference"
        if os.path.exists(epp_path):
            ZeusCoreBase.run_command("echo balance_performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference")

        gov = "powersave" if vendor == "intel" else "schedutil"
        
        if shutil.which("cpupower"):
            success, out, err = ZeusCoreBase.run_command(f"cpupower frequency-set -g {gov}")
            if vendor == "intel":
                ZeusCoreBase.run_command("echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/min_perf_pct")
            return success, log + f"✅ Governor restaurado a {gov.upper()} ({vendor}).\n"
        else:
            cmd = f"echo {gov} | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, log + f"✅ Governor restaurado a {gov.upper()} via sysfs.\n"

class SystemJanitor(ZeusCoreBase):
    """Limpieza universal de residuos de sistema."""
    
    @staticmethod
    def deep_clean():
        log = "🧹 Iniciando limpieza universal Zeus...\n"
        tasks = [
            ("sync", "Sincronizando discos"),
            ("echo 3 | sudo tee /proc/sys/vm/drop_caches", "Vaciando PageCache RAM"),
            ("journalctl --vacuum-time=1d", "Rotando logs de sistema"),
        ]
        
        if shutil.which("apt-get"):
            tasks.append(("apt-get clean", "Limpiando cache de paquetes apt"))
            
        success = True
        for cmd, desc in tasks:
            log += f"📦 {desc}...\n"
            try:
                if "|" in cmd:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    s, out, err = result.returncode == 0, result.stdout.strip(), result.stderr.strip()
                else:
                    s, out, err = ZeusCoreBase.run_command(cmd)
                
                if not s: success = False
                if out: log += f"  > {out}\n"
                if err: log += f"  ⚠️ {err}\n"
            except Exception as e:
                success = False
                log += f"  ❌ Error: {str(e)}\n"
        
        try:
            cache_path = os.path.expanduser("~/.cache")
            if os.path.exists(cache_path):
                log += "🗑️ Vaciando ~/.cache de usuario...\n"
                os.system(f"rm -rf {cache_path}/*")
                log += "  ✅ Cache de usuario limpia.\n"
        except: pass
            
        return success, log

class SensorPatch(ZeusCoreBase):
    """Parches adaptativos de hardware."""

    @staticmethod
    def apply_best_fix(is_x99=False):
        if is_x99:
            log = "🛠️ Aplicando optimización específica para X99...\n"
            success, grub_log = BootManager.apply_kernel_patch("nct6775.force_id=0xd42b", "Soporte Sensores X99")
            log += grub_log
            
            conf_path = "/etc/sensors.d/zeus_x99.conf"
            content = """# Configuración Zeus para X99
chip "nct6796-isa-0a20"
    ignore temp1
    ignore temp4
    ignore temp5
    ignore temp6
    ignore fan3
    ignore fan4
"""
            try:
                with open("/tmp/z_sensors", "w") as f: f.write(content)
                os.system(f"sudo mv /tmp/z_sensors {conf_path}")
                ZeusCoreBase.run_command("sensors -s")
                log += "✅ Mapeo de sensores X99 instalado.\n"
            except: pass
            return success, log
        else:
            return True, "💡 Hardware estándar: Optimizaciones de bus de sistema aplicadas.\n"

class ThermalManager(ZeusCoreBase):
    """Gestión de ventiladores inteligente."""

    @staticmethod
    def auto_configure():
        log = "🌀 Sincronizando sistema térmico...\n"
        
        if not shutil.which("fancontrol"):
            log += "📦 Instalando herramientas térmicas...\n"
            ZeusCoreBase.run_command("apt-get update && apt-get install -y lm-sensors fancontrol")

        try:
            if os.path.exists("/etc/fancontrol"):
                log += "✅ Configuración de /etc/fancontrol detectada.\n"
                log += "🔄 Reiniciando servicio para aplicar cambios...\n"
                s, out, err = ZeusCoreBase.run_command("systemctl restart fancontrol")
                log += f"{out or err or 'Servicio reiniciado con éxito.'}\n"
                return True, log
            else:
                log += "⚠️ No hay configuración de ventiladores (/etc/fancontrol).\n"
                log += "👉 Ve a la pestaña 'Scripts' y usa 'configure_fancontrol.sh'.\n"
                return True, log
        except Exception as e:
            return False, log + f"❌ Error: {str(e)}\n"

class NetworkManager(ZeusCoreBase):
    """Gestión de latencia de red."""
    
    @staticmethod
    def set_low_latency():
        log = "📡 Aplicando ajustes TCP Low Latency...\n"
        cmds = [
            "echo 3 | sudo tee /proc/sys/net/ipv4/tcp_fastopen",
            "echo 1 | sudo tee /proc/sys/net/ipv4/tcp_low_latency"
        ]
        success = True
        for cmd in cmds:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0: success = False
        return success, log + "✅ TCP FastOpen y Low Latency ACTIVADOS.\n"

    @staticmethod
    def set_default():
        log = "📡 Restaurando ajustes de red predeterminados...\n"
        cmds = [
            "echo 1 | sudo tee /proc/sys/net/ipv4/tcp_fastopen",
            "echo 0 | sudo tee /proc/sys/net/ipv4/tcp_low_latency"
        ]
        success = True
        for cmd in cmds:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0: success = False
        return success, log + "✅ TCP FastOpen y Low Latency restaurados (DEFAULT).\n"

class MasterOptimizer:
    """Orquestador del Combo Zeus (Modo Dios)."""
    @staticmethod
    def run_master_combo(is_x99=False):
        log = "⚡ ACTIVANDO MODO ZEUS (Rendimiento Máximo) ⚡\n"
        log += "========================================\n"
        
        SC, LC = CPUManager.set_performance()
        log += LC
        
        SN, LN = NetworkManager.set_low_latency()
        log += LN
        
        SystemJanitor.deep_clean() # Limpieza silente en el combo
        ThermalManager.auto_configure()
        
        log += "========================================\n"
        log += "🔥 SISTEMA EN MODO DIOS.\n"
        return SC and SN, log

    @staticmethod
    def revert_master_combo():
        log = "🍃 DESACTIVANDO MODO ZEUS (Regresando a Normalidad) ⚡\n"
        log += "========================================\n"
        
        SC, LC = CPUManager.set_balanced()
        log += LC
        
        SN, LN = NetworkManager.set_default()
        log += LN
        
        log += "========================================\n"
        log += "✅ SISTEMA EN MODO EQUILIBRADO.\n"
        return SC and SN, log
