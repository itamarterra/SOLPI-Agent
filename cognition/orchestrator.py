import time
import os
from cognition.memory import SOLPIMemory
from cognition.world_model import WorldModel
from cognition.goal_manager import GoalManager
from cognition.workflow_engine import WorkflowEngine
from cognition.computer_use_engine import ComputerUseEngine
from cognition.executor import Executor
from cognition.reflection import Reflection
from cognition.learning import Learning
from cognition.evolution_engine import EvolutionEngine
from tools.voice_core import VoiceCore
from registry.tool_registry import ToolRegistry
from plugins.manager import PluginManager

class Orchestrator:
    """
    O Cérebro Integrado SOLPI OS v5.0: O Ciclo de Auto-Aperfeiçoamento.
    """
    def __init__(self):
        self.voice = VoiceCore()
        self.memory = SOLPIMemory()
        self.registry = ToolRegistry()
        self.world = WorldModel(self.memory)
        self.goal_manager = GoalManager(self.memory)
        self.cue = ComputerUseEngine(self.memory, self.voice)
        self.executor = Executor(self.memory)
        self.reflection = Reflection(self.memory, self.voice)
        self.learning = Learning(self.memory)
        
        # Novos Motores v5.0
        self.evolution = EvolutionEngine(self.memory, self.registry)
        self.marketplace = PluginManager(self.registry)
        
        # Inicializa o mercado local
        self.marketplace.scan_and_load()

    def solve(self, objective):
        self.voice.speak(f"Comandante, objetivo aceito: {objective}.")

        # 1. PERCEPÇÃO & CONTEXTO
        self.world.update_state()
        self.goal_manager.set_goal(objective)

        # 2. PLANEJAMENTO DE FLUXO
        # Agora o workflow pode decidir se precisa criar uma nova ferramenta
        plan = self.workflow_decompose(objective)
        self.goal_manager.update_milestones(plan)

        # 3. EXECUÇÃO HÍBRIDA
        results = []
        for i, step in enumerate(plan):
            print(f"🏃 [ACTION]: {step['task']}")
            res = self.executor.run_plan([step])
            results.append(res)
            self.goal_manager.mark_step_complete(i)

        # 4. REFLEXÃO & AUDITORIA
        evaluation = self.reflection.evaluate_task(objective, results)

        # 5. AUTO-EVOLUÇÃO (A Mágica da v5.0)
        self.evolution.evolve_system(evaluation['feedback'])
        
        # 6. APRENDIZADO FINAL
        self.learning.record_experience(objective, plan, str(results), evaluation)

        self.voice.speak("Missão concluída. Eu aprendi algo novo com este processo.")
        return f"🏆 Objetivo '{objective}' finalizado e integrado à experiência."

    def workflow_decompose(self, objective):
        # Placeholder para a lógica do WorkflowEngine integrada
        return [{"id": 1, "task": objective, "agent": "ProgrammingAgent"}]
