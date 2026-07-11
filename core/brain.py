import os
import time
import threading

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
from core.model_registry import SOLPIModelRegistry
from core.capability_registry import SOLPICapabilityRegistry
from core.scheduler import SOLPIScheduler
from core.state_manager import SOLPIStateManager
from core.prompt_compiler import SOLPIPromptCompiler
from core.policy_engine import SOLPIPolicyEngine
from core.inference_engine import SOLPIInferenceEngine
from core.rag import SOLPIRAG
from core.context_engine import SOLPIContextEngine
from core.executor import SOLPIExecutor
from core.storage_layer import SOLPIStorageLayer
from core.evaluation_engine import SOLPIEvaluationEngine
from core.feature_store import SOLPIFeatureStore
from core.experts import InfraExpert, DevExpert, KnowledgeExpert, SQLExpert, VisionExpert
from core.formatter import SOLPIFormatter
from core.persona import SOLPIPersona

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v40.8 (AI Service Bus Architecture)
    Cérebro orquestrado via barramento de serviços de alta performance.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.service_bus = self.kernel.service_bus
        self.event_bus = self.kernel.event_bus # Link para compatibilidade
        
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.telemetry = SOLPITelemetry()
        self.knowledge = KnowledgeEngine(self)
        self.native_core = SOLPINeuralCore()
        
        # Infraestrutura de Plataforma
        self.model_registry = SOLPIModelRegistry(self)
        self.capability_registry = SOLPICapabilityRegistry(self)
        self.state_manager = SOLPIStateManager(self)
        self.scheduler = SOLPIScheduler(self)
        self.prompt_compiler = SOLPIPromptCompiler(self)
        self.policy_engine = SOLPIPolicyEngine(self)
        self.inference_engine = SOLPIInferenceEngine(self)
        self.rag = SOLPIRAG(self)
        self.context_engine = SOLPIContextEngine(self)
        self.executor = SOLPIExecutor(self)
        self.storage = SOLPIStorageLayer(self)
        self.evaluation = SOLPIEvaluationEngine(self)
        self.feature_store = SOLPIFeatureStore(self)
        
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.twin = SOLPIDigitalTwin(self)
        self.evolution = EvolutionEngine(self)
        self.learning = SOLPILearningLoop(self)
        self.supervisor = SOLPISupervisor(self)
        self.formatter = SOLPIFormatter()
        self.predictor = SOLPIPredictor(self)
        
        # Inscrições no Service Bus (Orquestração por Mensagens v40.8)
        self._setup_bus_subscriptions()
        
        # Especialistas Instanciados
        self.infra_expert = InfraExpert(self)
        self.dev_expert = DevExpert(self)
        self.knowledge_expert = KnowledgeExpert(self)
        self.sql_expert = SQLExpert(self)
        self.vision_expert = VisionExpert(self)
        
        self.scheduler.start(num_workers=2)
        self.scheduler.schedule(self.learning.start, priority=5, name="ContinuousLearning")

    def _setup_bus_subscriptions(self):
        """Assina tópicos para orquestração distribuída."""
        self.service_bus.subscribe("MEMORY_UPDATE", lambda msg: self.memory.add_episodic(msg.payload["role"], msg.payload["content"]))
        self.service_bus.subscribe("TELEMETRY_LOG", lambda msg: self.telemetry.log_request(msg.payload["tokens"]))
        self.service_bus.subscribe("EVALUATION_REQUEST", lambda msg: self.evaluation.evaluate_response(msg.payload["prompt"], msg.payload["resp"], msg.payload["start"]))

    def process(self, user_input):
        start_time = time.time()
        self.state_manager.transition_to("THINKING")
        
        # 1. Publica Entrada na Memória via Bus
        self.service_bus.publish("BRAIN", "MEMORY_UPDATE", {"role": "user", "content": user_input})
        
        # 2. Log de Telemetria via Bus
        tokens_count = len(user_input.split())
        self.service_bus.publish("BRAIN", "TELEMETRY_LOG", {"tokens": tokens_count})

        # 3. Comandos Rápidos (Dashboard/Twin)
        if any(x in user_input.lower() for x in ["stats", "performance"]):
            return self.formatter.format_response("TELEMETRY", str(self.telemetry.get_stats()))

        if "twin" in user_input.lower():
            return self.formatter.format_response("DIGITAL_TWIN", self.twin.get_3d_payload())

        # 4. Roteamento e Compilação
        expert_type, reason = self.supervisor.delegate(user_input)
        compiled_prompt = self.prompt_compiler.compile(user_input, expert_type, reason)

        # 5. Otimização Feature Store
        response_content = self.feature_store.get_feature(user_input)
        if response_content:
            response_content = response_content["data"]
        else:
            # 6. Execução
            allowed, _ = self.policy_engine.validate_action("PROMPT_INPUT", user_input)
            if not allowed: return "Ação Bloqueada por Política."

            if expert_type == "INFRA_EXPERT": response_content = self.infra_expert.run()
            elif expert_type == "SQL_EXPERT": response_content = self.sql_expert.run(user_input)
            elif expert_type == "VISION_EXPERT": response_content = self.vision_expert.run(user_input)
            else: response_content = "\n".join(self.tools.search(user_input)[:1])
            
            self.feature_store.save_feature(user_input, response_content)

        final_response = self.formatter.format_response(expert_type, response_content, reason)
        
        # 7. Dispara Avaliação via Bus (Assíncrono)
        self.service_bus.publish("BRAIN", "EVALUATION_REQUEST", {
            "prompt": compiled_prompt, "resp": final_response, "start": start_time
        })
        
        self.state_manager.transition_to("IDLE")
        return final_response
