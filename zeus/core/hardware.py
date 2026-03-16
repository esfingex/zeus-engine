import platform
import subprocess
import shutil
import os

class HardwareDetector:
    """Detecta componentes del sistema para optimizaciones específicas."""
    
    @staticmethod
    def get_distro():
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            return line.split("=")[1].strip().strip('"')
        except Exception:
            pass
        return platform.system()

    @staticmethod
    def get_gpu():
        try:
            lspci = subprocess.check_output("lspci", shell=True).decode()
            if "nvidia" in lspci.lower():
                return "NVIDIA"
            elif "amd" in lspci.lower() or "ati" in lspci.lower():
                return "AMD"
            return "Intel/Integrated"
        except Exception:
            return "Unknown"

    @staticmethod
    def get_nvidia_version():
        """Obtiene la versión del driver de NVIDIA si está disponible."""
        try:
            # Opción 1: nvidia-smi (comando oficial)
            if shutil.which("nvidia-smi"):
                res = subprocess.check_output("nvidia-smi --query-gpu=driver_version --format=csv,noheader", shell=True).decode()
                return res.strip()
            # Opción 2: Archivo del driver
            if os.path.exists("/proc/driver/nvidia/version"):
                with open("/proc/driver/nvidia/version") as f:
                    content = f.read()
                    # Parsing "NVRM version: NVIDIA UNIX x86_64 Kernel Module  535.129.03 ..."
                    return content.split("Module")[1].split("  ")[1].split(" ")[0].strip()
        except:
            pass
        return "N/A"

    @staticmethod
    def is_x99():
        """Detecta si es una placa X99/X79 sin requerir sudo si es posible."""
        try:
            paths = [
                "/sys/class/dmi/id/board_name",
                "/sys/class/dmi/id/product_name",
                "/sys/class/dmi/id/sys_vendor"
            ]
            for path in paths:
                if os.path.exists(path):
                    with open(path) as f:
                        content = f.read().lower()
                        if any(k in content for k in ["x99", "x79", "huananzhi", "jingsha", "machinist"]):
                            return True
        except Exception:
            pass

        try:
            if shutil.which("dmidecode"):
                output = subprocess.check_output("sudo -n dmidecode -t baseboard 2>/dev/null", shell=True, timeout=2).decode()
                keywords = ["X99", "X79", "Huananzhi", "Jingsha", "Machinist"]
                return any(k.lower() in output.lower() for k in keywords)
        except Exception:
            pass
        return False

    @staticmethod
    def get_cpu_info():
        info = {
            "processor": platform.processor() or "Unknown",
            "cores": str(os.cpu_count()),
            "architecture": platform.architecture()[0],
            "family": "N/A",
            "model": "N/A",
            "vendor": "N/A"
        }
        
        # Intentar sacar más detalle en Linux
        try:
            if os.path.exists("/proc/cpuinfo"):
                with open("/proc/cpuinfo") as f:
                    for line in f:
                        if "cpu family" in line:
                            info["family"] = line.split(":")[1].strip()
                        elif "model name" in line:
                            info["processor"] = line.split(":")[1].strip()
                        elif "model" in line and info["model"] == "N/A":
                             info["model"] = line.split(":")[1].strip()
                        elif "vendor_id" in line:
                            info["vendor"] = line.split(":")[1].strip()
        except Exception:
            pass
            
        return info
