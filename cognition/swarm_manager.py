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

    def _run_service(self, task, retry_count=0):
        agent_name = task['agent']
        max_retries = 1
        print(f"🛰️ [SERVICE]: Acionando microsserviço -> {agent_name} (Tentativa {retry_count + 1})")
        
        start_time = time.time()
        timestamp_start = datetime.now().isoformat()
        
        try:
            result = self.executor.run_plan([task])
            status = "completed"
        except Exception as e:
            if retry_count < max_retries:
                print(f"🔧 [SELF-HEALING]: Tentativa de recuperação para {agent_name}...")
                return self._run_service(task, retry_count + 1)
            
            # Protocolo de Substituição (Surrogate Fallback)
            surrogate_map = {
                "ClaudeAgent": "HermesAgent",
                "OpenClawAgent": "AutomationAgent",
                "HermesAgent": "ClaudeAgent"
            }
            
            surrogate = surrogate_map.get(agent_name)
            if surrogate:
                print(f"🛡️ [SELF-HEALING]: Microsserviço {agent_name} offline. Migrando missão para {surrogate}!")
                task['agent'] = surrogate
                return self._run_service(task, 0) # Tenta novamente com o substituto
            
            result = f"Failure: No surrogate available for {agent_name}"
            status = "failed"
            
        duration = time.time() - start_time
        self.tracer.log_trace(agent_name, task['task'], duration, status)
        
        return {
            "agent": agent_name,
            "task": task['task'],
            "status": status,
            "result": result,
            "metadata": {
                "started_at": timestamp_start,
                "finished_at": datetime.now().isoformat(),
                "latency": duration,
                "retries": retry_count
            }
        }
