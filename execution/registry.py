class SOLPICapabilityRegistry:
    """
    PACOTE 8100: CAPABILITY REGISTRY v50.0
    Catálogo central de Habilidades dos Agentes (O "Who is Who").
    """
    def __init__(self, brain):
        self.brain = brain
        self.capabilities = {
            "infra": {"agent": "InfraAgent", "tags": ["servidor", "zabbix", "docker", "rede"]},
            "sql": {"agent": "SQLAgent", "tags": ["banco", "dados", "chamado", "glpi"]},
            "code": {"agent": "DevAgent", "tags": ["python", "php", "refatorar", "codigo"]},
            "vision": {"agent": "VisionAgent", "tags": ["olhe", "veja", "tela", "print"]},
            "knowledge": {"agent": "KnowledgeAgent", "tags": ["como", "manual", "procedimento"]}
        }

    def resolve(self, query):
        """Encontra o agente mais capaz baseado na intenção."""
        query_low = query.lower()
        for cap, data in self.capabilities.items():
            if any(t in query_low for tag in data["tags"]):
                return data["agent"]
        return "Orchestrator"
