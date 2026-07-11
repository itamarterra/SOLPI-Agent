from intelligence.router import SOLPISemanticRouter

class SOLPISupervisor:
    """
    PACOTE 1603: AGENT SUPERVISOR v80.3 (Elite Coordination)
    Coordenador de Agentes Especialistas no Domínio de Execução.
    Hibridiza busca por Tags (Registry) e Roteamento Semântico.
    """
    def __init__(self, brain):
        self.brain = brain
        self.kernel = brain.kernel
        self.router = SOLPISemanticRouter(brain)

    def delegate(self, user_input):
        """Delega a tarefa para o Agente mais apto."""
        self.kernel.log_event("SUPERVISOR", f"Analisando delegação: {user_input[:20]}")
        
        # 1. Tenta correspondência exata por TAGS via Registry (Prioridade Alta)
        agent_from_registry = self.brain.capability_registry.resolve(user_input)
        if agent_from_registry != "GENERALIST":
            return agent_from_registry, "Identificado via assinatura de Tags (Registry)."
        
        # 2. Roteamento Inteligente (Similaridade Vetorial)
        agent_type, reason = self.router.route(user_input)
        
        # 3. Mapeamento para nomes de Agentes v80
        mapping = {
            "INFRA_EXPERT": "INFRA_AGENT",
            "SQL_EXPERT": "SQL_AGENT",
            "DEV_EXPERT": "DEV_AGENT",
            "VISION_EXPERT": "VISION_AGENT",
            "KNOWLEDGE_EXPERT": "KNOWLEDGE_AGENT",
            "solpi-engine": "SOLPI_ENGINE_AGENT"
        }
        
        final_agent = mapping.get(agent_type, agent_type)
        return final_agent, reason
