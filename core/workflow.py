import time

class SOLPIWorkflowEngine:
    """
    PACOTE 2203: WORKFLOW ENGINE v1.0
    Executa sequências de ações (Missões) com tratamento de erros.
    """
    def __init__(self, brain):
        self.brain = brain
        self.active_workflows = {}

    def run_mission(self, mission_name, steps):
        """Executa uma lista de passos (Etapa 1607)."""
        print(f"🎬 [WORKFLOW]: Iniciando missão '{mission_name}'...")
        results = []
        
        for i, step in enumerate(steps):
            print(f"  Step {i+1}: {step['desc']}...")
            try:
                # Executa a ação via Brain
                res = self.brain.execute_action(step)
                results.append({"step": i+1, "status": "OK", "result": res})
            except Exception as e:
                results.append({"step": i+1, "status": "FAIL", "error": str(e)})
                print(f"  🛑 [ERROR]: Falha no passo {i+1}. Abortando.")
                break
                
            time.sleep(1) # Pequena pausa entre passos
            
        return results
