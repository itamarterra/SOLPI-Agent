import time
import psutil
from datetime import datetime

class SOLPITelemetryEngine:
    """
    PACOTE 1900: TELEMETRY ENGINE v50.4
    Vigilância de alta resolução para o SOLPI-OS.
    Monitora Hardware, Tokens e Latência com histórico profundo.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.start_time = time.time()
        self.total_tokens = 0
        self.history = []

    def log_event(self, tokens, latency=0):
        self.total_tokens += tokens
        snapshot = {
            "t": time.time(),
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "tokens": tokens,
            "latency": latency
        }
        self.history.append(snapshot)
        if len(self.history) > 1000: self.history.pop(0)

    def get_snapshot(self):
        return {
            "uptime": f"{time.time() - self.start_time:.2f}s",
            "total_tokens": self.total_tokens,
            "current_cpu": f"{psutil.cpu_percent()}%",
            "current_ram": f"{psutil.virtual_memory().percent}%"
        }
