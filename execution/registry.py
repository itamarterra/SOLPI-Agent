class SOLPICapabilityRegistry:
    """
    PACOTE 8100: CAPABILITY REGISTRY v50.0
    Catálogo central de Habilidades dos Agentes (O "Who is Who").
    """
    def __init__(self, brain):
        self.brain = brain
        self.capabilities = {
            "infra": {"agent": "INFRA_AGENT", "tags": ["servidor", "zabbix", "docker", "rede"]},
            "sql": {"agent": "SQL_AGENT", "tags": ["banco", "dados", "chamado", "glpi"]},
            "code": {"agent": "DEV_AGENT", "tags": ["python", "php", "refatorar", "codigo"]},
            "vision": {"agent": "VISION_AGENT", "tags": ["olhe", "veja", "tela", "print"]},
            "knowledge": {"agent": "KNOWLEDGE_AGENT", "tags": ["como", "manual", "procedimento"]},
            "solpi_engine": {"agent": "SOLPI_ENGINE_AGENT", "tags": ["complexo", "navegar", "ferramentas", "agente de elite"]},
            "github": {"agent": "SOLPI_ENGINE_AGENT", "tags": ["github", "repositório", "git push", "pull request"]},
            "email": {"agent": "SOLPI_ENGINE_AGENT", "tags": ["enviar email", "correio", "outlook", "gmail"]},
            "automation": {"agent": "SOLPI_ENGINE_AGENT", "tags": ["automação", "fluxo complexo", "agendamento", "cron"]},
            "software_eng": {"agent": "SOLPI_ENGINE_AGENT", "tags": ["desenvolvimento", "refatorar sistema", "arquitetura"]},
            "auditor": {"agent": "AUDITOR_AGENT", "tags": ["auditoria", "relatório de sabedoria", "evolução", "status de conhecimento"]}
        }

    def resolve(self, query):
        """Encontra o agente mais capaz, incluindo ferramentas do motor de elite (v70.6)."""
        query_low = query.lower()
        
        # 1. Checa se a pergunta pede especificamente uma ferramenta do SOLPI-ENGINE
        try:
            elite_tools = self.brain.solpi_engine_agent.get_available_tools()
            if any(tool in query_low for tool in elite_tools):
                return "SOLPI_ENGINE_AGENT"
        except: pass

        # 2. Busca no registro padrão
        for cap, data in self.capabilities.items():
            if any(tag in query_low for tag in data["tags"]):
                return data["agent"]
                
        return "GENERALIST"
