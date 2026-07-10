import queue
import threading
import time

class SOLPIScheduler:
    """
    PACOTE 9000: AI TASK SCHEDULER v1.0
    Gerencia filas de prioridade para tarefas de Background, Learning e Execution.
    Inspirado em arquiteturas de sistemas distribuídos.
    """
    def __init__(self, brain):
        self.brain = brain
        self.priority_queue = queue.PriorityQueue()
        self.is_running = True
        self.workers = []

    def schedule(self, task_fn, priority=3, name="GenericTask"):
        """Adiciona uma tarefa na fila. 1=Crítica, 3=Normal, 5=Background."""
        self.priority_queue.put((priority, time.time(), name, task_fn))
        self.brain.kernel.log_event("SCHEDULER", f"Tarefa agendada: {name} (Prio: {priority})")

    def start(self, num_workers=2):
        for i in range(num_workers):
            t = threading.Thread(target=self._worker_loop, args=(i,), daemon=True)
            t.start()
            self.workers.append(t)

    def _worker_loop(self, worker_id):
        while self.is_running:
            try:
                priority, t_stamp, name, task_fn = self.priority_queue.get(timeout=1)
                self.brain.kernel.log_event("SCHEDULER", f"Worker-{worker_id} executando: {name}")
                task_fn()
                self.priority_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self.brain.kernel.log_event("ERROR", f"Falha na tarefa {name}: {e}")
