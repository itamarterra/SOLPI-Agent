import os
import time
import threading

from platform.kernel import SOLPIKernel
from execution.supervisor import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from intelligence.runtime import SOLPINeuralRuntime
from intelligence.loader import SOLPIModelLoader
from core.knowledge import KnowledgeEngine
from core.telemetry import SOLPITelemetry
from core.reflection import SOLPIReflectionEngine
from core.digital_twin import SOLPIDigitalTwin
from core.evolution import EvolutionEngine
from core.learning_loop import SOLPILearningLoop
from core.predictor import SOLPIPredictor
from core.model_registry import SOLPIModelRegistry
from execution.registry import SOLPICapabilityRegistry
from core.state_manager import SOLPIStateManager
from core.prompt_compiler import SOLPIPromptCompiler
from core.policy_engine import SOLPIPolicyEngine
from core.inference_engine import SOLPIInferenceEngine
from intelligence.rag import SOLPIRAG
from intelligence.context import SOLPIContextEngine
from execution.workflow import SOLPIWorkflowEngine
from intelligence.evaluation import SOLPIEvaluationEngine
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
    INTERFACE OPERACIONAL v50.3 (Platform Integrated)
    Cérebro orquestrado via domínios Platform, Intelligence e Execution.
    """
    def __init__(self):
        # 1. PLATFORM DOMAIN
        self.kernel = SOLPIKernel()
        self.service_bus = self.kernel.service_bus
        self.scheduler = self.kernel.scheduler
        self.storage = self.kernel.storage
        
        # 2. CORE ENGINES
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.telemetry = SOLPITelemetry()
        self.knowledge = KnowledgeEngine(self)
        self.native_core = SOLPINeuralRuntime()
        self.model_loader = SOLPIModelLoader(self)
        
        # 3. INTELLIGENCE DOMAIN
        self.model_registry = SOLPIModelRegistry(self)
        self.state_manager = SOLPIStateManager(self)
        self.prompt_compiler = SOLPIPromptCompiler(self)
        self.policy_engine = SOLPIPolicyEngine(self)
        self.inference_engine = SOLPIInferenceEngine(self)
        self.rag = SOLPIRAG(self)
        self.context_engine = SOLPIContextEngine(self)
        self.evaluation = SOLPIEvaluationEngine(self)
        self.feature_store = SOLPIFeatureStore(self)
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.evolution = EvolutionEngine(self)
        self.learning = SOLPILearningLoop(self)
        self.predictor = SOLPIPredictor(self)
        
        # 4. EXECUTION DOMAIN
        self.capability_registry = SOLPICapabilityRegistry(self)
        self.workflow = SOLPIWorkflowEngine(self)
        self.supervisor = SOLPISupervisor(self)
        self.formatter = SOLPIFormatter()
        
        # Especialistas Instanciados
        self.infra_agent = InfraAgent(self)
        self.dev_agent = DevAgent(self)
        self.vision_agent = VisionAgent(self)
        self.sql_agent = SQLAgent(self)
        self.knowledge_agent = KnowledgeAgent(self)
        
        # Start Background Services
        self._setup_bus_subscriptions()
        self.scheduler.start(workers=2)
        self.scheduler.schedule(self.learning.start, priority=5, name="ContinuousLearning")

    def _setup_bus_subscriptions(self):
        self.service_bus.subscribe("MEMORY_UPDATE", lambda msg: self.memory.add_episodic(msg.payload["role"], msg.payload["content"]))
        self.service_bus.subscribe("TELEMETRY_LOG", lambda msg: self.telemetry.log_request(msg.payload["tokens"]))
        self.service_bus.subscribe("EVALUATION_REQUEST", lambda msg: self.evaluation.evaluate_response(msg.payload["prompt"], msg.payload["resp"], msg.payload["start"]))

    def process(self, user_input):
        start_time = time.time()
        self.state_manager.transition_to("THINKING")
        self.service_bus.publish("BRAIN", "MEMORY_UPDATE", {"role": "user", "content": user_input})
        
        tokens_count = len(user_input.split())
        self.service_bus.publish("BRAIN", "TELEMETRY_LOG", {"tokens": tokens_count})

        if any(x in user_input.lower() for x in ["stats", "performance"]):
            return self.formatter.format_response("TELEMETRY", str(self.telemetry.get_stats()))

        # Execution Flow
        agent_type, reason = self.supervisor.delegate(user_input)
        compiled_prompt = self.prompt_compiler.compile(user_input, agent_type, reason)

        response_content = self.feature_store.get_feature(user_input)
        if response_content:
            response_content = response_content["data"]
        else:
            allowed, _ = self.policy_engine.validate_action("PROMPT_INPUT", user_input)
            if not allowed: return "Ação Bloqueada por Política."

            if agent_type == "INFRA_AGENT": response_content = self.infra_agent.run()
            elif agent_type == "SQL_AGENT": response_content = self.sql_agent.run(user_input)
            elif agent_type == "VISION_AGENT": response_content = self.vision_agent.run(user_input)
            elif agent_type == "DEV_AGENT": response_content = self.dev_agent.run(user_input)
            elif agent_type == "KNOWLEDGE_AGENT": response_content = self.knowledge_agent.run(user_input)
            else: response_content = "\n".join(self.tools.search(user_input)[:1])
            
            self.feature_store.save_feature(user_input, response_content)

        final_response = self.formatter.format_response(agent_type, response_content, reason)
        self.service_bus.publish("BRAIN", "EVALUATION_REQUEST", {"prompt": compiled_prompt, "resp": final_response, "start": start_time})
        
        self.state_manager.transition_to("IDLE")
        return final_response
