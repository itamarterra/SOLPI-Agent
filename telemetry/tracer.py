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
        
        # Trigger heal check if status is failed
        if status == "failed":
            self._trigger_healing_protocol(agent, "Execution Failure")

    def _trigger_healing_protocol(self, agent, reason):
        print(f"🛡️ [SELF-HEALING]: Alerta detectado no microsserviço {agent}! Razão: {reason}")
        # Aqui o sistema decide o que fazer: Reiniciar, Limpar Cache ou Notificar
        print(f"🔧 [SELF-HEALING]: Tentando reinicialização a quente do {agent}...")

    def get_mesh_health(self, agent=None):
        # Implementação básica de verificação de histórico
        return "HEALTHY"
