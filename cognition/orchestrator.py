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
from tools.voice_core import VoiceCore

class Orchestrator:
    """O Cérebro Integrado SOLPI OS v4.5: Voz, Visão e Auto-Recuperação."""
    
    def __init__(self):
        self.voice = VoiceCore()
        self.memory = SOLPIMemory()
        self.world = WorldModel(self.memory)
        self.goal_manager = GoalManager(self.memory)
        self.cue = ComputerUseEngine(self.memory, self.voice)
        self.executor = Executor(self.memory)
        self.planner = Planner(self.memory)
        self.workflow = WorkflowEngine(self.planner)
        self.reflection = Reflection(self.memory, self.voice)
        self.learning = Learning(self.memory)

    def solve(self, objective):
        # 0. VOZ: Confirmar recebimento
        self.voice.speak(f"Objetivo recebido: {objective}. Deixe comigo.")

        # 1. PERCEPÇÃO
        self.world.update_state()
        self.goal_manager.set_goal(objective)

        # 2. PLANEJAMENTO
        plan = self.workflow.decompose(objective, {"world": self.world.state})
        self.goal_manager.update_milestones(plan)

        # 3. EXECUÇÃO INTEGRADA (CUE + AUTO-RECOVERY)
        results = []
        for i, step in enumerate(plan):
            print(f"🏃 [ACTION]: Marco {i+1}/{len(plan)} -> {step['task']}")
            
            # Se for tarefa de interface, usa CUE com Auto-Recovery
            if any(x in step['task'].lower() for x in ["clique", "digite", "abra", "ícone"]):
                res = self.cue.execute_with_recovery("click" if "clique" in step['task'] else "type", {"text": step['task']})
            else:
                res = self.executor.run_plan([step])
            
            # Validação via Reflexão por etapa
            eval_res = self.reflection.evaluate_task(step['task'], res)
            if eval_res['status'] == 'retry':
                # Tenta re-executar a etapa uma vez no nível de orquestração
                res = self.executor.run_plan([step])

            results.append(res)
            self.goal_manager.mark_step_complete(i)

        # 4. FINALIZAÇÃO
        self.voice.speak(f"Itamar, o objetivo '{objective}' foi concluído.")
        return f"🏆 Missão cumprida: {objective}"
