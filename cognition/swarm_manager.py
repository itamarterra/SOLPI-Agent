import concurrent.futures
import time
from datetime import datetime
from telemetry.tracer import MeshTracer

class SwarmManager:
    """
    O Orquestrador de Microsserviços (Swarm Manager v6.1).
    Gerencia a execução paralela e isolada de múltiplos agentes com Rastreamento Total.
    """
    def __init__(self, executor):
        self.executor = executor
        self.max_workers = 10
        self.tracer = MeshTracer()

    def _run_service(self, task):
        agent_name = task['agent']
        print(f"🛰️ [SERVICE]: Acionando microsserviço -> {agent_name}")
        
        start_time = time.time()
        timestamp_start = datetime.now().isoformat()
        
        try:
            result = self.executor.run_plan([task])
            status = "completed"
        except Exception:
            result = "Failure during execution"
            status = "failed"
            
        duration = time.time() - start_time
        
        # Envia para o Tracer de Escala
        self.tracer.log_trace(agent_name, task['task'], duration, status)
        
        return {
            "agent": agent_name,
            "task": task['task'],
            "status": status,
            "result": result,
            "metadata": {
                "started_at": timestamp_start,
                "finished_at": datetime.now().isoformat(),
                "latency": duration
            }
        }
