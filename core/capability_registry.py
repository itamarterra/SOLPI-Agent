class SOLPICapabilityRegistry:
    """
    PACOTE 8100: CAPABILITY REGISTRY v1.0
    Catálogo central de tudo o que a IA sabe fazer (Skills, Tools, Experts).
    O "Who is Who" das habilidades do SOLPI-OS.
    """
    def __init__(self, brain):
        self.brain = brain
        self.capabilities = {
            "sql": {"expert": "SQLExpert", "desc": "Consultas em MariaDB/GLPI", "tags": ["banco", "dados", "chamado"]},
            "infra": {"expert": "InfraExpert", "desc": "Zabbix e Redes", "tags": ["servidor", "conexão", "docker"]},
            "code": {"expert": "DevExpert", "desc": "Geração e Correção de Código", "tags": ["python", "php", "patch"]},
            "vision": {"expert": "VisionExpert", "desc": "Análise de Tela", "tags": ["screenshot", "olhe", "veja"]}
        }

    def find_expert(self, query):
        """Busca o especialista baseado em tags e descrição (Semantic Route Base)."""
        query_low = query.lower()
        for cap, data in self.capabilities.items():
            if any(tag in query_low for tag in data["tags"]):
                return data["expert"]
        return "Generalist"
