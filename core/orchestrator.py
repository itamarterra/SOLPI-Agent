from core.semantic_router import SOLPISemanticRouter

class SOLPISupervisor:
    """
    PACOTE 1603: AGENT SUPERVISOR v40.2
    Agora utiliza Roteamento Semântico para delegação inteligente.
    """
    def __init__(self, brain):
        self.brain = brain
        self.kernel = brain.kernel
        self.router = SOLPISemanticRouter(brain)

    def delegate(self, user_input):
        self.kernel.log_event("SUPERVISOR", f"Iniciando análise semântica: {user_input[:30]}...")
        
        # 1. Tenta roteamento vetorial primeiro (v40.2)
        expert, reason = self.router.route(user_input)
        
        # 2. Fallback para regras manuais críticas (Zabbix/Emergência)
        if expert == "GENERALIST":
            cmd = user_input.lower()
            if any(x in cmd for x in ["banco", "servidor", "zabbix"]):
                return "INFRA_EXPERT", "Fallback: Detecção manual de infraestrutura crítica."
        
        return expert, reason
