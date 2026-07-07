import psutil
import platform
import os
import pygetwindow as gw
import pyautogui
from datetime import datetime

class WorldModel:
    """
    O Modelo de Mundo do SOLPI OS v4.0.
    Monitoramento contínuo e profundo do ambiente de execução.
    """
    def __init__(self, memory):
        self.memory = memory
        self.state = {}

    def update_state(self):
        """Captura o estado 360º do ambiente."""
        self.state = {
            "environment": {
                "os": platform.system(),
                "version": platform.version(),
                "user": os.getlogin(),
                "active_window": self._get_active_window(),
                "mouse_pos": pyautogui.position(),
                "monitors": self._get_monitors()
            },
            "resources": {
                "cpu": f"{psutil.cpu_percent()}%",
                "ram": f"{psutil.virtual_memory().percent}%",
                "disk": f"{psutil.disk_usage('/').percent}%",
                "internet": self._check_connectivity()
            },
            "services": {
                "docker": self._check_service("docker"),
                "glpi": self._check_connectivity("localhost:8081"), # Exemplo
                "zabbix": self._check_connectivity("localhost:8080") # Exemplo
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Sincroniza percepção com a Memória Semântica
        self.memory.store(
            content=f"World State Snapshot: {self.state['environment']['active_window']} active",
            layer="knowledge",
            tags="situational_awareness"
        )
        return self.state

    def _get_active_window(self):
        try: return gw.getActiveWindow().title
        except: return "Desktop"

    def _get_monitors(self):
        try:
            from screeninfo import get_monitors # pip install screeninfo
            return [{"name": m.name, "width": m.width, "height": m.height} for m in get_monitors()]
        except: return "Single Display"

    def _check_connectivity(self, host="8.8.8.8"):
        import socket
        try:
            # Tenta conexão simples de socket
            target = host.split(":")[0]
            port = int(host.split(":")[1]) if ":" in host else 53
            socket.create_connection((target, port), timeout=1)
            return "CONNECTED"
        except: return "OFFLINE"

    def _check_service(self, name):
        # Placeholder para checagem real de processos/serviços
        return "RUNNING"
