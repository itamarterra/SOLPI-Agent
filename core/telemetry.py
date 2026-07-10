import time
import psutil
from datetime import datetime

class SOLPITelemetry:
    """
    PACOTE 1906: TELEMETRY v1.0
    Coleta métricas de performance, tokens e saúde do OS.
    """
    def __init__(self):
        self.start_time = time.time()
        self.total_tokens = 0
        self.requests_count = 0

    def log_request(self, tokens):
        self.total_tokens += tokens
        self.requests_count += 1

    def get_stats(self):
        uptime = time.time() - self.start_time
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        return {
            "uptime": f"{uptime:.2f}s",
            "cpu_usage": f"{cpu}%",
            "ram_usage": f"{ram}%",
            "total_tokens": self.total_tokens,
            "avg_tokens_per_req": self.total_tokens / max(1, self.requests_count)
        }
