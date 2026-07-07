import time
import json
from cognition.memory import SOLPIMemory
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
from tools.voice_core import VoiceCore
from registry.tool_registry import ToolRegistry

class Orchestrator:
    """
    O AI CORE v6.0: O Cérebro Unificado.
    Integra Raciocínio LLM, Enxame de Agentes e Gêmeo Digital.
    """
    def __init__(self):
        # Motores de Inteligência (v6)
        self.llm = LLMEngine()
        self.intent = IntentAnalyzer(self.llm)
        
        # Sensores e Interface
        self.voice = VoiceCore()
        self.vision = VisionEngine()
        
        # Infraestrutura Cognitiva (v4-v5)
        self.memory = SOLPIMemory()
        self.temporal_memory = TemporalMemory()
        self.registry = ToolRegistry()
        self.world = WorldModel(self.memory)
        self.reasoner = Reasoner(self.memory)
        self.planner = Planner(self.memory)
        self.workflow = WorkflowEngine(self.planner, self.reasoner)
        self.experience = ExperienceEngine(self.memory)
        self.goal_manager = GoalManager(self.memory)
        self.executor = Executor(self.memory)
        self.reflection = Reflection(self.memory, self.voice)
        self.composer = SkillComposer(self.memory, self.registry)
        self.simulator = SimulationEngine(self.memory, self.world)
        self.executive = ExecutiveFunction()
        self.digital_twin = DigitalTwin(self.memory)
        self.swarm = SwarmManager(self.executor)

    def solve(self, user_input):
        start_time = time.time()
        self.executive.set_state("PENSANDO")
        
        # 1. PERCEPÇÃO MUNDIAL & DIGITAL TWIN
        world_state = self.world.update_state()
        self.digital_twin.sync_from_sources()
        
        # 2. ANÁLISE DE INTENÇÃO (LLM-CENTRIC v6)
        intent = self.intent.analyze(user_input, world_state)
        print(f"🎯 [INTENT]: {intent}")

        if intent == "CONVERSATION":
            return self._handle_conversation(user_input)

        # 3. CICLO DE EXECUÇÃO DE ELITE (Se for GOAL ou TROUBLESHOOTING)
        self.voice.speak(f"Processando objetivo estratégico: {user_input}")
        self.goal_manager.set_goal(user_input)

        # 4. PLANEJAMENTO HIERÁRQUICO (Task Tree)
        self.executive.set_state("PLANEJANDO")
        task_tree = self.workflow.generate_task_tree(user_input, world_state)
        self.goal_manager.update_milestones(task_tree['branches'])

        # 5. SIMULAÇÃO DE IMPACTO
        sim_report = self.simulator.simulate_plan(task_tree['branches'])
        if sim_report['predicted_success_rate'] < 50:
            msg = "Risco de falha crítica detectado. Abortando execução."
            self.voice.speak(msg)
            return f"❌ {msg}"

        # 6. EXECUÇÃO VIA ENXAME (Swarm Intelligence)
        self.executive.set_state("EXECUTANDO")
        swarm_results = self.swarm.execute_swarm(task_tree['branches'])
        
        for i, res in enumerate(swarm_results):
            self.goal_manager.mark_step_complete(i)

        # 7. REFLEXÃO & APRENDIZADO
        self.executive.set_state("OBSERVANDO")
        evaluation = self.reflection.evaluate_task(user_input, swarm_results)
        
        self.experience.distill({
            "problem": user_input,
            "context": world_state,
            "duration": time.time() - start_time,
            "result": str(swarm_results),
            "errors": [],
            "confidence": sim_report['predicted_success_rate']
        })

        self.executive.set_state("DORMINDO")
        final_msg = f"Objetivo concluído com {sim_report['predicted_success_rate']}% de confiança."
        return self._handle_conversation(f"O resultado do enxame foi: {final_msg}. Resuma para o usuário.")

    def _handle_conversation(self, text):
        messages = [
            {"role": "system", "content": "Você é o SOLPI OS v6.0. Responda de forma clara e técnica em Português-BR."},
            {"role": "user", "content": text}
        ]
        res = self.llm.chat(messages)
        try:
            msg = res['choices'][0]['message']['content']
            self.voice.speak(msg)
            return msg
        except:
            return "Cérebro em manutenção. Por favor, verifique sua chave de API."
