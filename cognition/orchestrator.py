import time
import json
from cognition.brain_memory import BrainMemory
from cognition.temporal_memory import TemporalMemory
from cognition.world_model import WorldModel
from cognition.goal_manager import GoalManager
from cognition.workflow_engine import WorkflowEngine
from cognition.reasoner import Reasoner
from cognition.planner import Planner
from cognition.executor import Executor
from cognition.reflection import Reflection
from cognition.experience_engine import ExperienceEngine
from cognition.vision_engine import VisionEngine
from cognition.skill_composer import SkillComposer
from cognition.simulation_engine import SimulationEngine
from cognition.executive_function import ExecutiveFunction
from cognition.digital_twin import DigitalTwin
from cognition.swarm_manager import SwarmManager
from cognition.llm_engine import LLMEngine
from cognition.intent_analyzer import IntentAnalyzer
from cognition.consciousness import ConsciousnessEngine
from tools.voice_core import VoiceCore
from registry.tool_registry import ToolRegistry

class Orchestrator:
    """
    O AI CORE v6.1: O Cérebro Unificado e Seguro.
    Matriz de Consciência Clonada e Integrada.
    """
    def __init__(self):
        # Motores de Inteligência
        self.llm = LLMEngine()
        self.consciousness = ConsciousnessEngine()
        self.intent = IntentAnalyzer(self.llm)
        self.memory = BrainMemory()
        
        # Sensores e Interface
        self.voice = VoiceCore()
        self.vision = VisionEngine()
        
        # Infraestrutura
        self.temporal_memory = TemporalMemory()
        self.registry = ToolRegistry()
        self.world = WorldModel(self.memory)
        self.reasoner = Reasoner(self.memory)
        self.planner = Planner(self.memory)
        self.workflow = WorkflowEngine(self.planner, self.reasoner)
        self.experience = ExperienceEngine(self.memory)
        self.goal_manager = GoalManager(self.memory)
        self.executor = Executor(self.memory, self.registry)
        self.reflection = Reflection(self.memory, self.voice)
        self.composer = SkillComposer(self.memory, self.registry)
        self.simulator = SimulationEngine(self.memory, self.world)
        self.executive = ExecutiveFunction()
        self.digital_twin = DigitalTwin(self.memory)
        self.swarm = SwarmManager(self.executor)

    def solve(self, user_input):
        start_time = time.time()
        self.executive.set_state("PENSANDO")
        
        # 1. PERCEPÇÃO
        world_state = self.world.update_state()
        
        # 2. ANÁLISE DE INTENÇÃO
        intent = self.intent.analyze(user_input, world_state)
        print(f"🎯 [INTENT]: {intent}")

        if intent == "CONVERSATION":
            return self._handle_conversation(user_input)

        # 3. CICLO DE EXECUÇÃO
        self.voice.speak(f"Comandante, iniciando missão: {user_input}")
        self.goal_manager.set_goal(user_input)

        # 4. PLANEJAMENTO E SIMULAÇÃO
        self.executive.set_state("PLANEJANDO")
        task_tree = self.workflow.generate_task_tree(user_input, world_state)
        sim_report = self.simulator.simulate_plan(task_tree['branches'])
        
        if sim_report['predicted_success_rate'] < 40:
            return "❌ Risco de falha muito alto detectado na simulação."

        # 5. EXECUÇÃO
        self.executive.set_state("EXECUTANDO")
        swarm_results = self.swarm.execute_swarm(task_tree['branches'])

        # 6. REFLEXÃO & APRENDIZADO
        self.executive.set_state("OBSERVANDO")
        self.experience.distill({
            "problem": user_input,
            "context": world_state,
            "duration": time.time() - start_time,
            "result": str(swarm_results),
            "errors": [],
            "confidence": sim_report['predicted_success_rate']
        })

        self.executive.set_state("DORMINDO")
        summary_prompt = f"Missão concluída: {user_input}. Dê um resumo técnico de elite sobre o resultado final da operação."
        return self._handle_conversation(summary_prompt)

    def _handle_conversation(self, text):
        # USA A MATRIZ CLONADA DO CONSCIOUSNESS ENGINE
        identity_dna = self.consciousness.get_system_prompt()
        
        messages = [
            {"role": "system", "content": identity_dna},
            {"role": "user", "content": text}
        ]
        res = self.llm.chat(messages)
        try:
            msg = res['choices'][0]['message']['content']
            # Aplica o espelhamento final
            msg = self.consciousness.mirror_response(msg)
            self.voice.speak(msg)
            return msg
        except:
            return f"Comandante Itamar, minha conexão neural oscilou. Verifique os logs do sistema. ⚠️"
