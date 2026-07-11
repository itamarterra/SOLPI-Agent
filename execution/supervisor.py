from intelligence.router import SOLPISemanticRouter

class SOLPISupervisor:
    """
    PACOTE 1603: AGENT SUPERVISOR v50.0
    Coordenador de Agentes Especialistas no Domínio de Execução.
    """
    def __init__(self, brain):
        self.brain = brain
        self.kernel = brain.kernel
        self.router = SOLPISemanticRouter(brain)

    def delegate(self, user_input):
        """Delega a tarefa para o Agente mais apto via Roteamento Semântico."""
        self.kernel.log_event("SUPERVISOR", f"Analisando delegação: {user_input[:20]}")
        
        # 1. Roteamento Inteligente
        agent_type, reason = self.router.route(user_input)
        
        # 2. Mapeamento para nomes de Agentes v50.0
        mapping = {
            "INFRA_EXPERT": "INFRA_AGENT",
            "SQL_EXPERT": "SQL_AGENT",
            "DEV_EXPERT": "DEV_AGENT",
            "VISION_EXPERT": "VISION_AGENT",
            "KNOWLEDGE_EXPERT": "KNOWLEDGE_AGENT"
        }
        
        final_agent = mapping.get(agent_type, agent_type)
        return final_agent, reason
