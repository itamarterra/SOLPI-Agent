import queue
import threading
import time

class SOLPITaskScheduler:
    """
    PACOTE 9000: AI TASK SCHEDULER v50.3
    Gerenciador de filas de execução migrado para a Plataforma.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.priority_queue = queue.PriorityQueue()
        self.active = True

    def schedule(self, task_fn, priority=3, name="Task"):
        self.priority_queue.put((priority, time.time(), name, task_fn))

    def start(self, workers=2):
        for i in range(workers):
            threading.Thread(target=self._worker, args=(i,), daemon=True).start()

    def _worker(self, id):
        while self.active:
            try:
                priority, _, name, fn = self.priority_queue.get(timeout=1)
                self.kernel.log_event("SCHEDULER", f"Worker-{id} executando {name}")
                fn()
                self.priority_queue.task_done()
            except queue.Empty: continue
            except Exception as e:
                self.kernel.log_event("ERROR", f"Tarefa {name} falhou: {e}")
