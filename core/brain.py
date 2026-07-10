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
from core.predictor import SOLPIPredictor
from core.experts import InfraExpert, DevExpert, KnowledgeExpert, SQLExpert, VisionExpert
from core.predictor import SOLPIPredictor
from core.model_registry import SOLPIModelRegistry
from core.capability_registry import SOLPICapabilityRegistry
from core.scheduler import SOLPIScheduler
from core.state_manager import SOLPIStateManager
from core.experts import InfraExpert, DevExpert, KnowledgeExpert, SQLExpert, VisionExpert
from core.formatter import SOLPIFormatter
from core.persona import SOLPIPersona
import threading

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v40.2 (Platform Infrastructure)
    Cérebro orquestrado com Scheduler e State Manager.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.telemetry = SOLPITelemetry()
        self.knowledge = KnowledgeEngine()
        self.native_core = SOLPINeuralCore()
        
        # 🟢 Registries & Infrastructure (v40.2)
        self.model_registry = SOLPIModelRegistry(self)
        self.capability_registry = SOLPICapabilityRegistry(self)
        self.state_manager = SOLPIStateManager(self)
        self.scheduler = SOLPIScheduler(self)
        
        self.event_bus = self.kernel.event_bus
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.twin = SOLPIDigitalTwin(self)
        self.evolution = EvolutionEngine(self)
        self.learning = SOLPILearningLoop(self)
        self.supervisor = SOLPISupervisor(self)
        self.formatter = SOLPIFormatter()
        self.predictor = SOLPIPredictor(self)
        
        # Especialistas Instanciados
        self.infra_expert = InfraExpert(self)
        self.dev_expert = DevExpert(self)
        self.knowledge_expert = KnowledgeExpert(self)
        self.sql_expert = SQLExpert(self)
        self.vision_expert = VisionExpert(self)
        
        # Inicia Infraestrutura de Background
        self.scheduler.start(num_workers=2)
        # Transfere o aprendizado para o Scheduler (Prioridade Baixa)
        self.scheduler.schedule(self.learning.start, priority=5, name="ContinuousLearning")

    def process(self, user_input):
        # 1. Recupera contexto da memória para "lembrar" do diálogo
        history = self.memory.short_term[-5:] # Últimas 5 interações
        context_summary = " | ".join([f"{h['r']}: {h['c']}" for h in history])
        
        self.memory.add_episodic("user", user_input)
        
        # 2. LOG DE TELEMETRIA
        tokens_count = len(user_input.split())
        self.telemetry.log_request(tokens_count)

        # 2. COMANDO DE MÉTRICAS / TWIN
        if any(x in user_input.lower() for x in ["stats", "métricas", "performance", "dashboard"]):
            stats = self.telemetry.get_stats()
            return self.formatter.format_response("TELEMETRY", "\n".join([f"- {k}: {v}" for k, v in stats.items()]))

        if "twin" in user_input.lower() or "3d" in user_input.lower():
            return self.formatter.format_response("DIGITAL_TWIN", f"🌐 Payload Gerado v40.0:\n{self.twin.get_3d_payload()}", "Sincronizando topologia 3D.")

        # 3. FLUXO PADRÃO (Delegação para Especialistas v40.0)
        expert_type, reason = self.supervisor.delegate(user_input)
        
        # 4. REFLECTION AUDIT
        self.reflection.audit_moe_routing(self.native_core.moe.routing_stats)

        # 5. EXECUÇÃO VIA ESPECIALISTA COM FORMATAÇÃO (Perfect Communication)
        response_content = ""
        expert_name = expert_type
        
        if expert_type == "INFRA_EXPERT":
            response_content = self.infra_expert.run()
        elif expert_type == "DEV_EXPERT":
            response_content = self.dev_expert.run(user_input)
        elif expert_type == "KNOWLEDGE_EXPERT":
            response_content = self.knowledge_expert.run(user_input)
        elif expert_type == "SQL_EXPERT":
            response_content = self.sql_expert.run(user_input)
        elif expert_type == "VISION_EXPERT":
            response_content = self.vision_expert.run(user_input)
        else:
            expert_name = "ORQUESTRADOR"
            search_res = self.tools.search(user_input)
            response_content = "🔍 Buscando informações externas:\n" + "\n".join(search_res[:2])

        # Aplica a formatação final "Perfect Communication"
        return self.formatter.format_response(expert_name, response_content, reason)

    def heartbeat_check(self):
        # 1. Auditoria de Saúde
        audit = self.tools.self_audit()
        # 2. Análise Preditiva
        self.predictor.check_and_alert()
        return audit
