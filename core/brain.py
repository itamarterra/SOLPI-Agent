import os
import time
import threading

from foundation.kernel import SOLPIKernel
from foundation.config import SOLPIConfig

from intelligence.runtime import SOLPINeuralRuntime
from intelligence.neural_vm import SOLPINeuralVM
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
from intelligence.guardrails import SOLPIGuardrails
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
from operations.profiler import SOLPINeuralProfiler
from operations.twin import SOLPIDigitalTwin
from operations.self_repair import SOLPISelfRepairEngine

from developer.gateway import SOLPIGateway
from developer.cli import SOLPICLI
from developer.sdk import SOLPISDK
from developer.formatter import SOLPIFormatter

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v60.0 (Singularity Platform)
    Orquestrador Supremo da malha de IA.
    """
    def __init__(self):
        # 1. FOUNDATION
        self.kernel = SOLPIKernel()
        self.config = SOLPIConfig()
        self.service_bus = self.kernel.service_bus
        self.event_bus = self.kernel.event_bus # Link para compatibilidade
        self.scheduler = self.kernel.scheduler
        self.storage = self.kernel.storage
        
        # 2. INTELLIGENCE (The Cérebro)
        self.native_core = SOLPINeuralRuntime(self.config)
        self.neural_vm = SOLPINeuralVM(self) # 🟢 Neural VM
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
        self.guardrails = SOLPIGuardrails(self) # 🟢 AI Guardrails
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
        
        # 3. OPERATIONS
        self.telemetry = SOLPITelemetryEngine(self.kernel)
        self.predictor = SOLPIPredictiveEngine(self)
        self.reflection = SOLPIReflectionEngine(self.kernel)
        self.profiler = SOLPINeuralProfiler(self) # 🟢 Profiler
        self.self_repair = SOLPISelfRepairEngine(self)
        self.twin = SOLPIDigitalTwin(self)
        
        # 4. EXECUTION
        self.capability_registry = SOLPICapabilityRegistry(self)
        self.workflow = SOLPIWorkflowEngine(self)
        self.supervisor = SOLPISupervisor(self)
        self.tools = AgentTools()
        
        # 5. DEVELOPER
        self.gateway = SOLPIGateway(self)
        self.cli = SOLPICLI(self)
        self.sdk = SOLPISDK(self)
        self.formatter = SOLPIFormatter()
        
        # Especialistas Instanciados (Execution Domain v60)
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
        # 1. AI Guardrails Check (v70.0 Hardened)
        safe, msg = self.guardrails.scan_prompt(user_input)
        if not safe:
            return self.formatter.format_response("SECURITY", msg, "Bloqueio preventivo de Prompt Injection.")

        start_time = time.time()
        pid = self.process_manager.spawn_thought(f"Query: {user_input[:15]}", "EXECUTION")
        
        self.state_manager.transition_to("THINKING")
        self.service_bus.publish("MEMORY_UPDATE", {"role": "user", "content": user_input}, sender="BRAIN")
        
        agent_type, reason = self.supervisor.delegate(user_input)
        
        # Logic execution...
        def execute_logic():
            if agent_type == "INFRA_AGENT": return self.infra_agent.run()
            elif agent_type == "SQL_AGENT": return self.sql_agent.run(user_input)
            elif agent_type == "VISION_AGENT": return self.vision_agent.run(user_input)
            elif agent_type == "DEV_AGENT": return self.dev_agent.run(user_input)
            elif agent_type == "KNOWLEDGE_AGENT": return self.knowledge_agent.run(user_input)
            return "Processamento concluído."

        response_content = self.executive.request_execution(f"Task_{agent_type}", 2, execute_logic)
        final_response = self.formatter.format_response(agent_type, response_content, reason)
        
        self.service_bus.publish("EVALUATION_REQUEST", {"prompt": "", "resp": final_response, "start": start_time}, sender="BRAIN")
        
        self.process_manager.terminate_thought(pid)
        self.state_manager.transition_to("IDLE")
        return final_response

    def heartbeat_check(self):
        audit = self.tools.self_audit()
        self.predictor.check_health()
        return audit
