import os
import importlib.util

class SOLPIPluginEngine:
    """
    PACOTE 2202: PLUGIN ENGINE v1.0
    Carregamento dinâmico de extensões corporativas.
    """
    def __init__(self, kernel, plugin_dir="plugins"):
        self.kernel = kernel
        self.plugin_dir = plugin_dir
        os.makedirs(self.plugin_dir, exist_ok=True)
        self.plugins = {}

    def discover_plugins(self):
        """Varre a pasta em busca de novos plugins (Etapa 1700)."""
        files = [f for f in os.listdir(self.plugin_dir) if f.endswith(".py")]
        for f in files:
            name = f[:-3]
            if name not in self.plugins:
                self.load_plugin(name)

    def load_plugin(self, name):
        path = os.path.join(self.plugin_dir, f"{name}.py")
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.plugins[name] = module
            self.kernel.log_event("PLUGIN", f"Plugin '{name}' carregado com sucesso.")
        except Exception as e:
            self.kernel.log_event("ERROR", f"Falha ao carregar plugin {name}: {e}")

    def execute_plugin(self, name, method, *args, **kwargs):
        if name in self.plugins:
            func = getattr(self.plugins[name], method, None)
            if func: return func(*args, **kwargs)
        return f"❌ Plugin ou método {name}.{method} não encontrado."
