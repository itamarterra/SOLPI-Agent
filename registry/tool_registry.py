class ToolRegistry:
    """
    O GRÁFICO DE CAPACIDADES (Capability Graph).
    Mapeia: O QUE pode ser feito e QUEM possui a perícia necessária.
    """
    def __init__(self):
        self.tools = {}
        self.capability_graph = {
            "IT_OPS": ["Instalar Programas", "Configurar Firewall", "Backup", "DB Query"],
            "GUI_NAV": ["Clicar em Ícones", "OCR", "Preencher Formulários"],
            "WEB_RESEARCH": ["Google Shopping", "YouTube Trends", "Preços"],
            "CODING": ["Refatorar PHP", "Validar Python", "Git Sync"]
        }
        self.reputation_scores = {}

    def register(self, agent_name, tool_name, description, params=None):
        """Registra uma ferramenta no sistema."""
        tool_id = f"{agent_name}.{tool_name}"
        self.tools[tool_id] = {
            "agent": agent_name,
            "name": tool_name,
            "description": description,
            "params": params or {}
        }

    def list_all(self):
        """Retorna todas as ferramentas registradas."""
        return self.tools

    def get_experts_for(self, task_type):
        """Retorna os agentes mais confiáveis para uma tarefa."""
        print(f"🕸️ [CAPABILITY GRAPH]: Buscando especialistas para {task_type}...")
        return ["WindowsAgent", "DatabaseAgent"]
