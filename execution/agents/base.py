class BaseAgent:
    """Classe base para todos os Agentes Especialistas do SOLPI-OS."""
    def __init__(self, brain):
        self.brain = brain
        self.kernel = brain.kernel
