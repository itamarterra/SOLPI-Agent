import os
import time
from datetime import datetime

from core.event_bus import SOLPIEventBus

class SOLPIKernel:
    """
    KERNEL DO SOLPI-OS v40.0
    Gerencia recursos, permissões e barramento de eventos.
    """
    def __init__(self):
        self.start_time = datetime.now()
        self.version = "40.0-ENTERPRISE"
        self.active_agents = []
        self.permissions_level = "ADMIN"
        self.event_bus = SOLPIEventBus(self) # Inicializa o barramento
        self.event_bus.start_listening()
        
    def log_event(self, layer, event):
        """Camada 9: Observabilidade"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{layer}] {event}\n"
        print(f"📡 [KERNEL]: {event}")
        with open("kernel_events.log", "a", encoding="utf-8") as f:
            f.write(log_entry)

    def authorize_action(self, action_type):
        """Camada 8: Segurança / RBAC"""
        self.log_event("SECURITY", f"Validando autorização para: {action_type}")
        return True # Por enquanto, Diretor tem acesso total

    def get_uptime(self):
        return str(datetime.now() - self.start_time)
