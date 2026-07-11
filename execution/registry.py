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
            "knowledge": {"agent": "KnowledgeAgent", "tags": ["como", "manual", "procedimento"]},
            "hermes": {"agent": "HERMES_AGENT", "tags": ["complexo", "navegar", "ferramentas", "agente de elite"]},
            "github": {"agent": "HERMES_AGENT", "tags": ["github", "repositório", "git push", "pull request"]},
            "email": {"agent": "HERMES_AGENT", "tags": ["enviar email", "correio", "outlook", "gmail"]},
            "automation": {"agent": "HERMES_AGENT", "tags": ["automação", "fluxo complexo", "agendamento", "cron"]},
            "software_eng": {"agent": "HERMES_AGENT", "tags": ["desenvolvimento", "refatorar sistema", "arquitetura"]}
        }

    def resolve(self, query):
        """Encontra o agente mais capaz baseado na intenção."""
        query_low = query.lower()
        for cap, data in self.capabilities.items():
            if any(t in query_low for tag in data["tags"]):
                return data["agent"]
        return "Orchestrator"
