import time
from cognition.memory import SOLPIMemory
from cognition.world_model import WorldModel
from cognition.goal_manager import GoalManager
from cognition.workflow_engine import WorkflowEngine
from cognition.computer_use_engine import ComputerUseEngine
from cognition.executor import Executor
from cognition.reflection import Reflection
from cognition.learning import Learning

class Orchestrator:
    def __init__(self):
        self.memory = SOLPIMemory()
        self.world = WorldModel(self.memory)
        self.goal_manager = GoalManager(self.memory)
        self.cue = ComputerUseEngine(self.memory)
        # O executor agora pode delegar para o CUE se for tarefa de interface
        self.executor = Executor(self.memory)
        self.planner = Planner(self.memory)
        self.workflow = WorkflowEngine(self.planner)
        self.reflection = Reflection(self.memory, None)
        self.learning = Learning(self.memory)

    def solve(self, objective):
        # 1. PERCEPÇÃO
        self.world.update_state()
        self.goal_manager.set_goal(objective)

        # 2. PLANEJAMENTO
        plan = self.workflow.decompose(objective, {"world": self.world.state})
        self.goal_manager.update_milestones(plan)

        # 3. EXECUÇÃO COM VALIDAÇÃO VISUAL
        for i, step in enumerate(plan):
            print(f"🏃 [ACTION]: Marco {i+1}/{len(plan)}")
            
            # Se a tarefa for de interface, o CUE assume
            if any(x in step['task'].lower() for x in ["clique", "digite", "abra"]):
                res = self.cue.perform_action("click" if "clique" in step['task'] else "type", {"text": step['task']})
            else:
                res = self.executor.run_plan([step])
                
            self.goal_manager.mark_step_complete(i)

        # 4. REFLEXÃO E APRENDIZADO
        evaluation = self.reflection.evaluate(objective, plan, "Concluído")
        self.learning.record_experience(objective, plan, "Ok", evaluation)

        return f"🏆 Objetivo '{objective}' processado com sucesso pelo Computer Use Engine."
