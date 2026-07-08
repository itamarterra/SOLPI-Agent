import time
import json
from datetime import datetime

class MeshTracer:
    """
    Rastreador de Performance da Malha de Microsserviços.
    Mede latência, sucesso e carga de cada agente.
    """
    def __init__(self):
        self.trace_log = "logs/mesh_traces.jsonl"
        import os
        os.makedirs("logs", exist_ok=True)

    def log_trace(self, agent, task, duration, status):
        trace_data = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "task": task[:50],
            "latency_sec": round(duration, 3),
            "status": status,
            "node": "Trinity-Core-Main"
        }
        
        with open(self.trace_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace_data) + "\n")
        
        print(f"📊 [TRACER]: Trace registrado para {agent} | Latência: {trace_data['latency_sec']}s")

    def get_mesh_health(self):
        # Futuramente: Analisa os últimos traces para ver se algum motor está lento
        return "HEALTHY"
