import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.telemetry import SOLPITelemetry
from core.reflection import SOLPIReflectionEngine
from core.digital_twin import SOLPIDigitalTwin
from core.evolution import EvolutionEngine
from core.learning_loop import SOLPILearningLoop
import threading

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v40.0 (Ultimate Enterprise)
    Cérebro com Auto-Evolução, Twin 3D e Continuous Learning.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.telemetry = SOLPITelemetry()
        self.knowledge = KnowledgeEngine()
        self.native_core = SOLPINeuralCore()
        self.event_bus = self.kernel.event_bus
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.twin = SOLPIDigitalTwin(self)
        self.evolution = EvolutionEngine(self)
        self.learning = SOLPILearningLoop(self) # Motor de Aprendizado
        self.supervisor = SOLPISupervisor(self)
        
        # Inicia o aprendizado em thread separada
        threading.Thread(target=self.learning.start, daemon=True).start()

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        
        # 1. LOG DE TELEMETRIA (Etapa 1901)
        tokens_count = len(user_input.split()) # Estimativa simples
        self.telemetry.log_request(tokens_count)

        # 2. COMANDO DE MÉTRICAS / TWIN
        if any(x in user_input.lower() for x in ["stats", "métricas", "performance", "dashboard"]):
            stats = self.telemetry.get_stats()
            return "📊 [DASHBOARD]:\n" + "\n".join([f"- {k}: {v}" for k, v in stats.items()])

        if "twin" in user_input.lower() or "3d" in user_input.lower():
            return f"🌐 [DIGITAL TWIN v40.0]: Payload Gerado.\n{self.twin.get_3d_payload()}"

        # 3. FLUXO PADRÃO
        expert, _ = self.supervisor.delegate(user_input)
        
        # 4. REFLECTION AUDIT (v40.0)
        # Auditoria rápida das estatísticas do MoE após cada pensamento
        self.reflection.audit_moe_routing(self.native_core.moe.routing_stats)

        if expert == "INFRA_EXPERT": return self.tools.self_audit()

        return "🧠 [ORQUESTRADOR]: " + "\n".join(self.tools.search(user_input)[:1])

    def heartbeat_check(self):
        return self.tools.self_audit()
