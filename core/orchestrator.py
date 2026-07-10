class SOLPISupervisor:
    """
    PACOTE 1603: AGENT SUPERVISOR v3.0
    Coordena Especialistas em Pesquisa, Código e Infraestrutura.
    """
    def __init__(self, brain):
        self.brain = brain
        self.kernel = brain.kernel

    def delegate(self, user_input):
        cmd = user_input.lower()
        self.kernel.log_event("SUPERVISOR", f"Iniciando delegação para: {user_input[:20]}...")

        # 1. Especialista em Infraestrutura (Zabbix/Docker)
        if any(x in cmd for x in ["banco", "servidor", "status", "reinicie", "zabbix"]):
            return "INFRA_EXPERT", "Analisando telemetria e integridade de containers."

        # 2. Especialista em Desenvolvimento (Python/PHP)
        if any(x in cmd for x in ["código", "python", "php", "corrija", "script"]):
            return "DEV_EXPERT", "Iniciando análise de sintaxe e lógica de engenharia."

        # 3. Especialista em Conhecimento (RAG/Documentação)
        if any(x in cmd for x in ["como", "manual", "procedimento", "baixe"]):
            return "KNOWLEDGE_EXPERT", "Consultando base de dados corporativa e RAG."

        # 4. Especialista em SQL (Banco GLPI)
        if any(x in cmd for x in ["listar", "quem", "chamado", "ticket", "computador", "ativo", "documente", "registre"]):
            return "SQL_EXPERT", "Acessando banco de dados MariaDB/GLPI para extração ou documentação de dados."

        # 5. Especialista em Visão (Captura e Interface)
        if any(x in cmd for x in ["tela", "veja", "olhe", "clique", "print", "screenshot"]):
            return "VISION_EXPERT", "Ativando visão computacional para análise de interface."

        return "GENERALIST", "Processamento neural genérico."
