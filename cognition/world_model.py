import psutil
import platform
import os
import pygetwindow as gw
import pyautogui
from datetime import datetime

class WorldModel:
    """
    O Modelo de Mundo do SOLPI OS.
    Monitoramento contínuo do ambiente.
    """
    def __init__(self, memory):
        self.memory = memory
        self.state = {}

    def update_state(self):
        """Captura o estado 360º do ambiente."""
        self.state = {
            "environment": {
                "os": platform.system(),
                "active_window": self._get_active_window(),
                "mouse_pos": str(pyautogui.position()),
            },
            "resources": {
                "cpu": f"{psutil.cpu_percent()}%",
                "ram": f"{psutil.virtual_memory().percent}%",
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Usa o novo método 'record'
        self.memory.record(
            content=f"Snapshot: {self.state['environment']['active_window']} ativo.",
            tags="situational_awareness"
        )
        return self.state

    def _get_active_window(self):
        try: return gw.getActiveWindow().title
        except: return "Desktop"
