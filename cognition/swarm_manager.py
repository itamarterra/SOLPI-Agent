import threading
import queue
import time

class SwarmManager:
    """
    Gestor de Enxame de Agentes (Swarm Intelligence) v5.3.
    Coordena múltiplos agentes trabalhando em paralelo para resolver sub-objetivos.
    """
    def __init__(self, executor):
        self.executor = executor
        self.results_queue = queue.Queue()

    def execute_swarm(self, task_list):
        """Dispara múltiplos agentes em paralelo para as tarefas fornecidas."""
        threads = []
        print(f"🐝 [SWARM]: Disparando enxame de {len(task_list)} agentes...")

        for task in task_list:
            thread = threading.Thread(
                target=self._worker_thread,
                args=(task,)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        final_results = []
        while not self.results_queue.empty():
            final_results.append(self.results_queue.get())

        return final_results

    def _worker_thread(self, task):
        """Thread individual para cada agente do enxame."""
        agent_name = task['agent']
        print(f"   ➤ [SWARM UNIT]: {agent_name} iniciando tarefa: {task['task']}")
        
        start_time = time.time()
        # O executor lida com a instância do agente
        result = self.executor.run_plan([task])
        duration = time.time() - start_time
        
        self.results_queue.put({
            "task": task['task'],
            "agent": agent_name,
            "result": result,
            "duration": duration
        })
