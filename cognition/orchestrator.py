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
from tools.voice_core import VoiceCore
from registry.tool_registry import ToolRegistry

class Orchestrator:
    """
    O AI CORE v5.2: O Operador de Elite.
    Agora com Memória Temporal, Simulação de Planos e Funções Executivas.
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

    def solve(self, objective):
        start_time = time.time()
        self.executive.set_state("PENSANDO")
        self.voice.speak(f"Analisando objetivo: {objective}")

        # 1. PERCEPÇÃO & REGISTRO TEMPORAL
        world_state = self.world.update_state()
        cpu_val = float(world_state['resources']['cpu'].replace('%', ''))
        self.temporal_memory.record_metric("system", "cpu_usage", cpu_val)
        
        # 2. GESTÃO DE OBJETIVO
        self.goal_manager.set_goal(objective)

        # 3. PLANEJAMENTO HIERÁRQUICO
        self.executive.set_state("PLANEJANDO")
        task_tree = self.workflow.generate_task_tree(objective, world_state)
        self.goal_manager.update_milestones(task_tree['branches'])

        # 4. SIMULAÇÃO (Dry Run)
        sim_report = self.simulator.simulate_plan(task_tree['branches'])
        if sim_report['predicted_success_rate'] < 50:
            self.voice.speak("Risco muito alto detectado na simulação. Abortando execução física.")
            return "❌ Execução abortada por alto risco."

        # 5. EXECUÇÃO ORQUESTRADA COM VIGILÂNCIA DE RECURSOS
        self.executive.set_state("EXECUTANDO")
        results = []
        for i, task in enumerate(task_tree['branches']):
            # Proteção de Hardware
            ok, msg = self.executive.manage_resources(cpu_val, 0) # RAM fixo 0 por simplificação
            if not ok:
                self.voice.speak(msg)
                break
                
            res = self.executor.run_plan([task])
            results.append(res)
            self.goal_manager.mark_step_complete(i)

        # 6. REFLEXÃO & APRENDIZADO
        self.executive.set_state("OBSERVANDO")
        evaluation = self.reflection.evaluate_task(objective, results)
        self.experience.distill({
            "problem": objective,
            "context": world_state,
            "duration": time.time() - start_time,
            "result": str(results),
            "errors": [],
            "confidence": sim_report['predicted_success_rate']
        })

        self.executive.set_state("DORMINDO")
        return f"🏆 Objetivo concluído. Taxa de sucesso simulada foi de {sim_report['predicted_success_rate']}%."
