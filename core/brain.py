import os
import time
import threading

from platform.kernel import SOLPIKernel
from intelligence.runtime import SOLPINeuralRuntime
from intelligence.trainer import SOLPITrainer
from intelligence.rag import SOLPIRAG
from intelligence.context import SOLPIContextEngine
from intelligence.evaluation import SOLPIEvaluationEngine
from execution.supervisor import SOLPISupervisor
from execution.registry import SOLPICapabilityRegistry
from execution.workflow import SOLPIWorkflowEngine
from operations.telemetry import SOLPITelemetryEngine
from operations.predictor import SOLPIPredictiveEngine
from operations.reflection import SOLPIReflectionEngine
from operations.twin import SOLPIDigitalTwin
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
    INTERFACE OPERACIONAL v50.4 (Full Domain Migration)
    Cérebro orquestrado via domínios Platform, Intelligence, Execution e Operations.
    """
    def __init__(self):
        # 1. PLATFORM
        self.kernel = SOLPIKernel()
        self.service_bus = self.kernel.service_bus
        self.scheduler = self.kernel.scheduler
        self.storage = self.kernel.storage
        
        # 2. INTELLIGENCE
        self.native_core = SOLPINeuralRuntime()
        self.trainer = SOLPITrainer(self)
        self.rag = SOLPIRAG(self)
        self.context_engine = SOLPIContextEngine(self)
        self.evaluation = SOLPIEvaluationEngine(self)
        self.memory = AgentMemory()
        self.model_registry = SOLPIModelRegistry(self)
        self.inference_engine = SOLPIInferenceEngine(self)
        
        # 3. OPERATIONS
        self.telemetry = SOLPITelemetryEngine(self.kernel)
        self.predictor = SOLPIPredictiveEngine(self)
        self.gateway = SOLPIGateway(self) # 🟢 Gateway
        self.cli = SOLPICLI(self)         # 🟢 CLI
        self.sdk = SOLPISDK(self)         # 🟢 SDK
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.twin = SOLPIDigitalTwin(self)
        
        # 4. EXECUTION
        self.capability_registry = SOLPICapabilityRegistry(self)
        self.workflow = SOLPIWorkflowEngine(self)
        self.supervisor = SOLPISupervisor(self)
        
        # Utilities
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

    def process(self, user_input):
        start_time = time.time()
        self.state_manager.transition_to("THINKING")
        self.service_bus.publish("BRAIN", "MEMORY_UPDATE", {"role": "user", "content": user_input})
        
        agent_type, reason = self.supervisor.delegate(user_input)
        compiled_prompt = self.prompt_compiler.compile(user_input, agent_type, reason)
        
        # Logic execution...
        if agent_type == "INFRA_AGENT": response_content = self.infra_agent.run()
        elif agent_type == "SQL_AGENT": response_content = self.sql_agent.run(user_input)
        else: response_content = "Processamento concluído."

        final_response = self.formatter.format_response(agent_type, response_content, reason)
        
        self.telemetry.log_event(len(user_input.split()), time.time() - start_time)
        self.state_manager.transition_to("IDLE")
        return final_response
