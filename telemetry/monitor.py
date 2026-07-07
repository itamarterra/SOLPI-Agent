import psutil
import time
import json
from datetime import datetime

class OSMonitor:
    """
    Sistema de Observabilidade do SOLPI OS.
    Coleta métricas de performance e saúde do sistema.
    """
    def __init__(self):
        self.start_time = time.time()

    def get_system_metrics(self):
        return {
            "uptime": f"{time.time() - self.start_time:.2f}s",
            "cpu_usage": f"{psutil.cpu_percent()}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "disk_free": f"{psutil.disk_usage('/').free / (1024**3):.2f} GB",
            "timestamp": datetime.now().isoformat()
        }

    def log_metric(self, agent_name, duration, success):
        """Registra performance por agente."""
        log_entry = {
            "agent": agent_name,
            "duration": duration,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        with open("logs/telemetry.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
