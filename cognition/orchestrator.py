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
from tools.voice_core import VoiceCore
from registry.tool_registry import ToolRegistry

class Orchestrator:
    """
    O AI CORE v5.3: O Maestro do Enxame e Gêmeo Digital.
    Integração total de infraestrutura e inteligência coletiva.
    """
    def __init__(self):
        self.voice = VoiceCore()
        self.memory = SOLPIMemory()
        self.temporal_memory = TemporalMemory()
        self.registry = ToolRegistry()
        self.world = WorldModel(self.memory)
        self.vision = VisionEngine()
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
        
        # Módulos v5.3
        self.digital_twin = DigitalTwin(self.memory)
        self.swarm = SwarmManager(self.executor)

    def solve(self, objective):
        start_time = time.time()
        self.executive.set_state("PENSANDO")
        
        # 1. SINCRONIA DO GÊMEO DIGITAL (Contexto de TI)
        self.digital_twin.sync_from_sources()
        
        # 2. PERCEPÇÃO MUNDIAL
        world_state = self.world.update_state()
        self.voice.speak(f"Comandante, analisando objetivo sob a ótica do Gêmeo Digital.")

        # 3. GESTÃO DE OBJETIVO E PLANEJAMENTO
        self.goal_manager.set_goal(objective)
        task_tree = self.workflow.generate_task_tree(objective, world_state)
        self.goal_manager.update_milestones(task_tree['branches'])

        # 4. SIMULAÇÃO E IMPACTO
        sim_report = self.simulator.simulate_plan(task_tree['branches'])
        impact = self.digital_twin.predict_impact("execution", "core_infra")
        
        if sim_report['predicted_success_rate'] < 50:
            self.voice.speak("Risco de impacto na infraestrutura detectado. Abortando.")
            return "❌ Execução abortada por segurança do Gêmeo Digital."

        # 5. EXECUÇÃO VIA ENXAME (SWARM INTELLIGENCE)
        self.executive.set_state("EXECUTANDO")
        self.voice.speak(f"Disparando enxame de agentes para {objective}.")
        
        # Executa as tarefas em paralelo usando o Swarm Manager
        swarm_results = self.swarm.execute_swarm(task_tree['branches'])
        
        for i, res in enumerate(swarm_results):
            self.goal_manager.mark_step_complete(i)

        # 6. REFLEXÃO & APRENDIZADO
        self.executive.set_state("OBSERVANDO")
        evaluation = self.reflection.evaluate_task(objective, swarm_results)
        
        self.experience.distill({
            "problem": objective,
            "context": world_state,
            "duration": time.time() - start_time,
            "result": str(swarm_results),
            "errors": [],
            "confidence": sim_report['predicted_success_rate']
        })

        self.executive.set_state("DORMINDO")
        self.voice.speak(f"Objetivo alcançado em {time.time() - start_time:.2f} segundos através do enxame.")
        return f"🏆 Sucesso coletivo atingido. {len(swarm_results)} agentes cooperaram."
