from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Classe base para todos os agentes especializados do SOLPI-AIOS.
    """
    def __init__(self, memory):
        self.memory = memory
        self.tools = {}
        self.register_tools()

    @abstractmethod
    def register_tools(self):
        """Cada agente deve registrar suas capacidades aqui."""
        pass

    @abstractmethod
    def execute(self, task_description):
        """Cada agente interpreta e executa a tarefa à sua maneira."""
        pass

    def log_activity(self, activity):
        """Registra o que o agente fez na memória de experiência."""
        self.memory.remember(
            content=f"[{self.__class__.__name__}] {activity}",
            layer="experience"
        )
