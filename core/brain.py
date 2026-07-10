import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.event_bus import SOLPIEventBus
from core.experts import InfraExpert, DevExpert, KnowledgeExpert, SQLExpert

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v37.0 (EDA & Gateway)
    Integrado com Barramento de Eventos e API Externa.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.bus = SOLPIEventBus(self.kernel) # Novo Barramento!
        self.native_core = SOLPINeuralCore()
        self.supervisor = SOLPISupervisor(self)
        self.infra_expert = InfraExpert(self)
        
        # Subscreve para eventos críticos
        self.bus.subscribe("DB_DOWN", lambda data: self.infra_expert.run())
        self.bus.start_listening()

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        cmd = user_input.lower().strip()
        
        # 1. EMITE EVENTO (Se for algo importante)
        if "alerta" in cmd: self.bus.publish("SYSTEM_ALERT", {"msg": user_input})

        # 2. FLUXO DE SUPERVISÃO
        expert_tag, _ = self.supervisor.delegate(user_input)
        if expert_tag == "INFRA_EXPERT": return self.infra_expert.run()

        # 3. GLOBAL FALLBACK
        results = self.tools.search(user_input)
        return "🧠 [ORQUESTRADOR]: " + "\n".join(results[:1])

    def heartbeat_check(self):
        audit = self.tools.self_audit()
        if "OFFLINE" in str(audit):
            self.bus.publish("DB_DOWN", {"status": "critical"})
        return audit
