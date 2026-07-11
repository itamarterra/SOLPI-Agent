import time
import queue

class SOLPITask:
    """Representação de uma unidade de trabalho com prioridade e contexto."""
    def __init__(self, name, priority, action, args=None, context=None):
        self.name = name
        self.priority = priority # 1 (Crítico) a 5 (Background)
        self.action = action
        self.args = args or []
        self.context = context or {}
        self.created_at = time.time()

class SOLPIExecutiveFunction:
    """
    PACOTE 5200: EXECUTIVE FUNCTION ENGINE v50.8
    Inspirado na neurociência: gerencia a "Atenção Executiva" do SOLPI-OS.
    Controla prioridades, interrupções e a alternância entre tarefas (Task Switching).
    """
    def __init__(self, brain):
        self.brain = brain
        self.task_queue = queue.PriorityQueue()
        self.current_focus = None
        self.interrupt_allowed = True

    def evaluate_priority(self, new_task_name, proposed_priority):
        """Avalia se uma nova tarefa deve interromper o foco atual."""
        if not self.current_focus:
            return True
            
        # Se a nova tarefa for mais prioritária (valor menor), permite interrupção
        if proposed_priority < self.current_focus.priority:
            self.brain.kernel.log_event("EXECUTIVE", f"⚠️ INTERRUPÇÃO: {new_task_name} sobrepõe {self.current_focus.name}")
            return True
            
        return False

    def request_execution(self, name, priority, action, args=None):
        """Solicita execução de uma tarefa ao sistema."""
        task = SOLPITask(name, priority, action, args)
        
        if self.evaluate_priority(name, priority):
            # Salva o foco atual de volta na fila se houver
            if self.current_focus:
                self.task_queue.put((self.current_focus.priority, self.current_focus))
            
            self.current_focus = task
            self.brain.state_manager.transition_to("EXECUTING")
            return self._execute_now(task)
        else:
            self.brain.kernel.log_event("EXECUTIVE", f"⏳ Agendando: {name} (Fila de Espera)")
            self.task_queue.put((priority, task))
            return "Tarefa agendada para execução posterior."

    def _execute_now(self, task):
        """Executa a tarefa imediatamente no foco central."""
        start = time.time()
        try:
            result = task.action(*task.args)
            duration = time.time() - start
            self.brain.kernel.log_event("EXECUTIVE", f"✅ Concluído: {task.name} em {duration:.2f}s")
            
            # Após concluir, tenta pegar a próxima da fila
            self.current_focus = None
            self._resume_next()
            
            return result
        except Exception as e:
            self.brain.kernel.log_event("ERROR", f"Falha executiva em {task.name}: {e}")
            self.current_focus = None
            return f"Erro na execução: {e}"

    def _resume_next(self):
        """Retoma a próxima tarefa da fila de prioridade."""
        if not self.task_queue.empty():
            _, next_task = self.task_queue.get()
            self.brain.kernel.log_event("EXECUTIVE", f"🔄 Retomando: {next_task.name}")
            self.request_execution(next_task.name, next_task.priority, next_task.action, next_task.args)
        else:
            self.brain.state_manager.transition_to("IDLE")
