import time
from datetime import datetime

class ExecutiveFunction:
    """
    O Córtex Pré-Frontal do SOLPI OS.
    Gerencia: Prioridades, Tempo, Conflitos e o Estado Cognitivo.
    """
    STATES = ["DORMINDO", "PENSANDO", "PLANEJANDO", "EXECUTANDO", "OBSERVANDO", "RECUPERANDO", "INVESTIGANDO"]

    def __init__(self):
        self.current_state = "DORMINDO"
        self.priority_queue = []
        self.resource_limit = 0.8 # 80% de CPU/RAM
        self.active_tasks = {}

    def set_state(self, state):
        if state in self.STATES:
            self.current_state = state
            print(f"🧠 [COGNITIVE STATE]: {state}")

    def manage_resources(self, cpu_usage, ram_usage):
        """Impede o Agente de travar o computador do Itamar."""
        if cpu_usage > 90 or ram_usage > 95:
            self.set_state("RECUPERANDO")
            return False, "Sobrecarga detectada. Pausando execução."
        return True, "Recursos OK"

    def negotiate_task(self, task_name, estimated_risk):
        """Avalia se uma tarefa deve ser interrompida ou priorizada."""
        if estimated_risk == "Alto":
            self.set_state("INVESTIGANDO")
            return "Tarefa de alto risco. Requer simulação profunda."
        return "Tarefa autorizada."
