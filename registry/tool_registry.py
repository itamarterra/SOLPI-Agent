class ToolRegistry:
    """
    O GRÁFICO DE CAPACIDADES (Capability Graph).
    Mapeia: O QUE pode ser feito e QUEM possui a perícia necessária.
    """
    def __init__(self):
        self.capability_graph = {
            "IT_OPS": ["Instalar Programas", "Configurar Firewall", "Backup", "DB Query"],
            "GUI_NAV": ["Clicar em Ícones", "OCR", "Preencher Formulários"],
            "WEB_RESEARCH": ["Google Shopping", "YouTube Trends", "Preços"],
            "CODING": ["Refatorar PHP", "Validar Python", "Git Sync"]
        }
        self.reputation_scores = {}

    def get_experts_for(self, task_type):
        """Retorna os agentes mais confiáveis para uma tarefa."""
        # Ex: "Quem é o especialista em IT_OPS com melhor reputação?"
        print(f"🕸️ [CAPABILITY GRAPH]: Buscando especialistas para {task_type}...")
        return ["WindowsAgent", "DatabaseAgent"] # Exemplo estático para base

    def register_tool(self, tool_metadata):
        """
        Metadados Detalhados (Sugestão CTO):
        name, risk, estimated_time, requires_admin, etc.
        """
        pass
