import os
import subprocess
import importlib.util

class PluginManager:
    """Gestiona la carga de módulos y scripts externos con soporte de Manifest."""
    
    def __init__(self, plugins_dir):
        self.plugins_dir = plugins_dir
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

    def discover_plugins(self):
        """Busca archivos .py y extrae su metadata (Manifest)."""
        plugins = []
        if not os.path.exists(self.plugins_dir):
            return plugins

        for file in os.listdir(self.plugins_dir):
            path = os.path.join(self.plugins_dir, file)
            
            # SOLO LEER PYTHON
            if not file.endswith(".py"):
                continue
            
            # Metadata por defecto
            info = {
                "file": file,
                "name": file,
                "description": "Script externo sin descripción.",
                "category": "General",
                "type": "python"
            }

            try:
                spec = importlib.util.spec_from_file_location("plugin_meta", path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "MANIFEST"):
                    manifest = getattr(module, "MANIFEST")
                    info["name"] = manifest.get("name", info["name"])
                    info["description"] = manifest.get("description", info["description"])
                    info["category"] = manifest.get("category", info["category"])
                    info["author"] = manifest.get("author", "Unknown")
                    info["version"] = manifest.get("version", "1.0")
            except Exception as e:
                print(f"⚠️ Error al leer manifest de {file}: {e}")
            
            plugins.append(info)
                
        return plugins

    def run_plugin(self, plugin_file):
        """Ejecuta un plugin basado en su archivo."""
        path = os.path.join(self.plugins_dir, plugin_file)
        
        if plugin_file.endswith(".py"):
            spec = importlib.util.spec_from_file_location("plugin_run", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "run"):
                import sys
                from io import StringIO
                
                old_stdout = sys.stdout
                redirected_output = StringIO()
                sys.stdout = redirected_output
                
                try:
                    res = module.run()
                    sys.stdout = old_stdout
                    output = redirected_output.getvalue()
                    return {"success": True, "stdout": output, "result": res}
                except Exception as e:
                    sys.stdout = old_stdout
                    return {"success": False, "stderr": str(e)}
                    
        return {"success": False, "stderr": "Formato no compatible o archivo no econtrado."}
