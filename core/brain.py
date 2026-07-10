import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.telemetry import SOLPITelemetry

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v39.0 (Observability & Math)
    Cérebro com telemetria ativa e motor matemático expandido.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.telemetry = SOLPITelemetry() # Telemetria!
        self.knowledge = KnowledgeEngine()
        self.native_core = SOLPINeuralCore()
        self.supervisor = SOLPISupervisor(self)

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        
        # 1. LOG DE TELEMETRIA (Etapa 1901)
        tokens_count = len(user_input.split()) # Estimativa simples
        self.telemetry.log_request(tokens_count)

        # 2. COMANDO DE MÉTRICAS
        if any(x in user_input.lower() for x in ["stats", "métricas", "performance", "dashboard"]):
            stats = self.telemetry.get_stats()
            return "📊 [DASHBOARD]:\n" + "\n".join([f"- {k}: {v}" for k, v in stats.items()])

        # 3. FLUXO PADRÃO
        expert, _ = self.supervisor.delegate(user_input)
        if expert == "INFRA_EXPERT": return self.tools.self_audit()

        return "🧠 [ORQUESTRADOR]: " + "\n".join(self.tools.search(user_input)[:1])

    def heartbeat_check(self):
        return self.tools.self_audit()
