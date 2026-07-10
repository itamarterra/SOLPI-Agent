import time

class SOLPIExecutor:
    """
    PACOTE 8800: WORKFLOW EXECUTOR v1.0
    Transforma planos em ações reais com segurança (Rollback/Retry).
    """
    def __init__(self, brain):
        self.brain = brain

    def execute_workflow(self, plan):
        """
        Executa uma lista de tarefas.
        plan: list de {"step": "name", "action": func, "args": []}
        """
        results = []
        self.brain.state_manager.transition_to("EXECUTING")
        
        for step in plan:
            success = False
            retries = 2
            
            while not success and retries >= 0:
                try:
                    self.brain.kernel.log_event("EXECUTOR", f"Iniciando: {step['step']}")
                    res = step['action'](*step.get('args', []))
                    results.append({"step": step['step'], "status": "OK", "result": res})
                    success = True
                except Exception as e:
                    self.brain.kernel.log_event("ERROR", f"Falha no passo {step['step']}: {e}")
                    retries -= 1
                    if retries < 0:
                        self.handle_rollback(results)
                        return {"status": "FAILED", "history": results}
                    time.sleep(1) # Pausa antes do retry

        self.brain.state_manager.transition_to("IDLE")
        return {"status": "SUCCESS", "history": results}

    def handle_rollback(self, history):
        """Tenta reverter ações em caso de erro crítico."""
        self.brain.kernel.log_event("SECURITY", "Iniciando Rollback de Segurança...")
        for action in reversed(history):
            self.brain.kernel.log_event("ROLLBACK", f"Desfazendo: {action['step']}")
            # Lógica de compensação entraria aqui
