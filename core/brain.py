import os
import time
import threading

from foundation.kernel import SOLPIKernel
from foundation.config import SOLPIConfig

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
from intelligence.memory import AgentMemory
from intelligence.model_registry import SOLPIModelRegistry
from intelligence.state import SOLPIStateManager
from intelligence.compiler import SOLPIPromptCompiler
from intelligence.inference import SOLPIInferenceEngine
from intelligence.feature_store import SOLPIFeatureStore
from intelligence.evolution import EvolutionEngine
from intelligence.learning import SOLPILearningLoop
from intelligence.knowledge import KnowledgeEngine
from intelligence.persona import SOLPIPersona
from intelligence.social import SOLPISocialEngine

from execution.supervisor import SOLPISupervisor
from execution.registry import SOLPICapabilityRegistry
from execution.workflow import SOLPIWorkflowEngine
from execution.agents.infra import InfraAgent
from execution.agents.dev import DevAgent
from execution.agents.vision import VisionAgent
from execution.agents.sql import SQLAgent
from execution.agents.knowledge import KnowledgeAgent
from execution.tools import AgentTools

from operations.telemetry import SOLPITelemetryEngine
from operations.predictor import SOLPIPredictiveEngine
from operations.reflection import SOLPIReflectionEngine
from operations.twin import SOLPIDigitalTwin
from operations.self_repair import SOLPISelfRepairEngine
from operations.profiler import SOLPINeuralProfiler

from developer.gateway import SOLPIGateway
from developer.cli import SOLPICLI
from developer.sdk import SOLPISDK
from developer.formatter import SOLPIFormatter

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v70.1 (Social Singularity)
    Cérebro orquestrado com foco em Diálogo e Execução Especializada.
    """
    def __init__(self):
        # 1. FOUNDATION
        self.kernel = SOLPIKernel()
        self.config = SOLPIConfig()
        self.service_bus = self.kernel.service_bus
        self.event_bus = self.kernel.service_bus
        self.scheduler = self.kernel.scheduler
        self.storage = self.kernel.storage
        
        # 2. INTELLIGENCE
        self.native_core = SOLPINeuralRuntime(self.config)
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
        self.state_manager = SOLPIStateManager(self)
        self.prompt_compiler = SOLPIPromptCompiler(self)
        self.inference_engine = SOLPIInferenceEngine(self)
        self.feature_store = SOLPIFeatureStore(self)
        self.evolution = EvolutionEngine(self)
        self.learning = SOLPILearningLoop(self)
        self.knowledge = KnowledgeEngine(self)
        self.persona = SOLPIPersona()
        self.social_engine = SOLPISocialEngine(self) # 🟢 Social Engine
        
        # 3. OPERATIONS
        self.telemetry = SOLPITelemetryEngine(self.kernel)
        self.predictor = SOLPIPredictiveEngine(self)
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.profiler = SOLPINeuralProfiler(self)
        self.self_repair = SOLPISelfRepairEngine(self)
        self.twin = SOLPIDigitalTwin(self)
        
        # 4. EXECUTION
        self.capability_registry = SOLPICapabilityRegistry(self)
        self.workflow = SOLPIWorkflowEngine(self)
        self.supervisor = SOLPISupervisor(self)
        self.tools = AgentTools()
        
        # Agentes
        self.infra_agent = InfraAgent(self)
        self.dev_agent = DevAgent(self)
        self.vision_agent = VisionAgent(self)
        self.sql_agent = SQLAgent(self)
        self.knowledge_agent = KnowledgeAgent(self)
        
        # 5. DEVELOPER
        self.gateway = SOLPIGateway(self)
        self.cli = SOLPICLI(self)
        self.sdk = SOLPISDK(self)
        self.formatter = SOLPIFormatter()
        
        self._setup_bus_subscriptions()
        self.scheduler.start(workers=2)

    def _setup_bus_subscriptions(self):
        self.service_bus.subscribe("MEMORY_UPDATE", lambda msg: self.memory.add_episodic(msg.payload["role"], msg.payload["content"]))
        self.service_bus.subscribe("TELEMETRY_LOG", lambda msg: self.telemetry.log_event(msg.payload["tokens"]))

    def process(self, user_input):
        start_time = time.time()
        pid = self.process_manager.spawn_thought(f"Query: {user_input[:15]}", "COGNITION")
        self.state_manager.transition_to("THINKING")
        
        # Registra na memória
        self.service_bus.publish("MEMORY_UPDATE", {"role": "user", "content": user_input}, sender="BRAIN")
        
        # 1. Tenta Delegação para Especialistas
        agent_type, reason = self.supervisor.delegate(user_input)
        
        # 2. Lógica de Execução com Fallback Conversacional
        def execute_logic():
            if agent_type == "INFRA_AGENT": return self.infra_agent.run()
            elif agent_type == "SQL_AGENT": return self.sql_agent.run(user_input)
            elif agent_type == "VISION_AGENT": return self.vision_agent.run(user_input)
            elif agent_type == "DEV_AGENT": return self.dev_agent.run(user_input)
            elif agent_type == "KNOWLEDGE_AGENT": return self.knowledge_agent.run(user_input)
            
            # Se for Generalista, usamos o Inference Engine (CONVERSA REAL)
            return self.chat_logic(user_input)

        response_content = self.executive.request_execution(f"Chat_{agent_type}", 2, execute_logic)
        final_response = self.formatter.format_response(agent_type, response_content, reason)
        
        self.process_manager.terminate_thought(pid)
        self.state_manager.transition_to("IDLE")
        return final_response

    def chat_logic(self, user_input):
        """Motor de Diálogo do SOLPI-OS."""
        # 1. Tenta o Corpus de Diálogo (Perguntas e Respostas da área criada)
        social_response = self.social_engine.get_response(user_input)
        if social_response:
            return social_response

        # 2. Se não estiver no corpus, tenta o Inference Engine Real (Qwen/Native)
        return self.inference_engine.execute(user_input, model_name=self.config.MODEL_TYPE)

    def heartbeat_check(self):
        try: return self.tools.self_audit()
        except: return []
