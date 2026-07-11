import os
import time
import threading

from platform.kernel import SOLPIKernel
from intelligence.runtime import SOLPINeuralRuntime
from intelligence.trainer import SOLPITrainer
from intelligence.rag import SOLPIRAG
from intelligence.context import SOLPIContextEngine
from intelligence.evaluation import SOLPIEvaluationEngine
from intelligence.cognitive import SOLPICognitiveEngine
from intelligence.executive import SOLPIExecutiveFunction
from intelligence.causal import SOLPICausalEngine
from intelligence.architecture import SOLPISelfArchitecture
from intelligence.hypothesis import SOLPIHypothesisEngine
from intelligence.trust import SOLPITrustNetwork
from intelligence.process_manager import SOLPICognitiveProcessManager
from execution.supervisor import SOLPISupervisor
from execution.registry import SOLPICapabilityRegistry
from execution.workflow import SOLPIWorkflowEngine
from operations.telemetry import SOLPITelemetryEngine
from operations.predictor import SOLPIPredictiveEngine
from operations.reflection import SOLPIReflectionEngine
from operations.twin import SOLPIDigitalTwin
from operations.self_repair import SOLPISelfRepairEngine
from developer.gateway import SOLPIGateway
from developer.cli import SOLPICLI
from developer.sdk import SOLPISDK

from core.memory import AgentMemory
from core.tools import AgentTools
from intelligence.loader import SOLPIModelLoader
from core.knowledge import KnowledgeEngine
from core.evolution import EvolutionEngine
from core.learning_loop import SOLPILearningLoop
from core.model_registry import SOLPIModelRegistry
from core.state_manager import SOLPIStateManager
from core.prompt_compiler import SOLPIPromptCompiler
from core.policy_engine import SOLPIPolicyEngine
from core.inference_engine import SOLPIInferenceEngine
from core.feature_store import SOLPIFeatureStore
from execution.agents.infra import InfraAgent
from execution.agents.dev import DevAgent
from execution.agents.vision import VisionAgent
from execution.agents.sql import SQLAgent
from execution.agents.knowledge import KnowledgeAgent
from core.formatter import SOLPIFormatter
from core.persona import SOLPIPersona

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v51.0 (Singularity Core)
    Cérebro de Singularidade com Consciência, Reputação e Auto-Cura Proativa.
    """
    def __init__(self):
        # 1. PLATFORM
        self.kernel = SOLPIKernel()
        self.service_bus = self.kernel.service_bus
        self.scheduler = self.kernel.scheduler
        self.storage = self.kernel.storage
        
        # 2. INTELLIGENCE (Cognitive Singularity)
        self.native_core = SOLPINeuralRuntime()
        self.trainer = SOLPITrainer(self)
        self.rag = SOLPIRAG(self)
        self.context_engine = SOLPIContextEngine(self)
        self.evaluation = SOLPIEvaluationEngine(self)
        self.cognitive = SOLPICognitiveEngine(self)
        self.executive = SOLPIExecutiveFunction(self)
        self.causal = SOLPICausalEngine(self)
        self.architecture = SOLPISelfArchitecture(self)
        self.hypothesis = SOLPIHypothesisEngine(self)
        self.trust = SOLPITrustNetwork(self)
        self.process_manager = SOLPICognitiveProcessManager(self)
        self.memory = AgentMemory()
        self.model_registry = SOLPIModelRegistry(self)
        self.inference_engine = SOLPIInferenceEngine(self)
        
        # 3. OPERATIONS
        self.telemetry = SOLPITelemetryEngine(self.kernel)
        self.predictor = SOLPIPredictiveEngine(self)
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.self_repair = SOLPISelfRepairEngine(self)
        self.twin = SOLPIDigitalTwin(self)
        
        # 4. EXECUTION
        self.capability_registry = SOLPICapabilityRegistry(self)
        self.workflow = SOLPIWorkflowEngine(self)
        self.supervisor = SOLPISupervisor(self)
        
        # 5. DEVELOPER
        self.gateway = SOLPIGateway(self)
        self.cli = SOLPICLI(self)
        self.sdk = SOLPISDK(self)
        
        # Base Helpers
        self.tools = AgentTools()
        self.knowledge = KnowledgeEngine(self)
        self.state_manager = SOLPIStateManager(self)
        self.prompt_compiler = SOLPIPromptCompiler(self)
        self.policy_engine = SOLPIPolicyEngine(self)
        self.feature_store = SOLPIFeatureStore(self)
        self.evolution = EvolutionEngine(self)
        self.learning = SOLPILearningLoop(self)
        self.formatter = SOLPIFormatter()
        
        # Specialists
        self.infra_agent = InfraAgent(self)
        self.dev_agent = DevAgent(self)
        self.vision_agent = VisionAgent(self)
        self.sql_agent = SQLAgent(self)
        self.knowledge_agent = KnowledgeAgent(self)
        
        self._setup_bus_subscriptions()
        self.scheduler.start(workers=2)
        self.scheduler.schedule(self.learning.start, priority=5, name="ContinuousLearning")

    def _setup_bus_subscriptions(self):
        self.service_bus.subscribe("MEMORY_UPDATE", lambda msg: self.memory.add_episodic(msg.payload["role"], msg.payload["content"]))
        self.service_bus.subscribe("TELEMETRY_LOG", lambda msg: self.telemetry.log_event(msg.payload["tokens"]))
        self.service_bus.subscribe("TRAINING_ANOMALY", lambda msg: self.self_repair.diagnose_and_fix(msg.payload))

    def process(self, user_input):
        start_time = time.time()
        pid = self.process_manager.spawn_thought(f"Query: {user_input[:15]}", "EXECUTION")
        
        self.state_manager.transition_to("THINKING")
        self.service_bus.publish("BRAIN", "MEMORY_UPDATE", {"role": "user", "content": user_input})
        
        agent_type, reason = self.supervisor.delegate(user_input)
        
        # Trust Layer: Avalia se a fonte do comando (RAG ou Usuário) é confiável
        trust_score = self.trust.evaluate_source("USER_ITAMAR")
        
        # Executive Execution
        def execute_logic():
            if agent_type == "INFRA_AGENT": return self.infra_agent.run()
            elif agent_type == "SQL_AGENT": return self.sql_agent.run(user_input)
            elif agent_type == "VISION_AGENT": return self.vision_agent.run(user_input)
            elif agent_type == "DEV_AGENT": return self.dev_agent.run(user_input)
            elif agent_type == "KNOWLEDGE_AGENT": return self.knowledge_agent.run(user_input)
            return "Processamento concluído."

        response_content = self.executive.request_execution(f"Task_{agent_type}", 2, execute_logic)
        final_response = self.formatter.format_response(agent_type, response_content, reason)
        
        self.process_manager.terminate_thought(pid)
        self.state_manager.transition_to("IDLE")
        return final_response
