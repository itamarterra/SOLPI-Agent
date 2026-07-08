import requests
from agents.base_agent import BaseAgent

class GLPIAgent(BaseAgent):
    """
    Agente especialista em gestão de tickets e ativos no GLPI.
    """
    def register_tools(self):
        if self.registry:
            self.registry.register("GLPIAgent", "create_ticket", "Abre um novo chamado no GLPI")
            self.registry.register("GLPIAgent", "list_tickets", "Lista chamados abertos")

    def execute(self, task_description):
        print(f"🎫 [GLPI AGENT]: Operando -> {task_description}")
        
        if "chamado" in task_description.lower() or "ticket" in task_description.lower():
            return "GLPI: Chamado #456 criado com sucesso."
            
        return "GLPIAgent: Tarefa processada."
