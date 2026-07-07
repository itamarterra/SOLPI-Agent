import psutil
import platform
import os
import pygetwindow as gw
from datetime import datetime

class WorldModel:
    """
    O Modelo de Mundo do SOLPI OS.
    Mantém o estado atual do ambiente Windows, Hardware e Rede.
    """
    def __init__(self, memory):
        self.memory = memory
        self.state = {}

    def update_state(self):
        """Atualiza a percepção do agente sobre o PC e a Web."""
        self.state = {
            "os": platform.system(),
            "active_window": self._get_active_window(),
            "open_apps": self._get_open_apps(),
            "cpu_usage": f"{psutil.cpu_percent()}%",
            "ram_free": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            "internet": self._check_internet(),
            "docker_status": self._check_docker(),
            "timestamp": datetime.now().isoformat()
        }
        # Salva o estado na Memória Semântica para análise de contexto futura
        self.memory.store(str(self.state), layer="knowledge", tags="world_state")
        return self.state

    def _get_active_window(self):
        try: return gw.getActiveWindow().title
        except: return "Unknown"

    def _get_open_apps(self):
        return [w.title for w in gw.getAllWindows() if w.title]

    def _check_internet(self):
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except: return False

    def _check_docker(self):
        import subprocess
        try:
            res = subprocess.run("docker ps", shell=True, capture_output=True)
            return res.returncode == 0
        except: return False
