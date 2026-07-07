import time
import json
from cognition.memory import SOLPIMemory
from cognition.world_model import WorldModel
from cognition.goal_manager import GoalManager
from cognition.workflow_engine import WorkflowEngine
from cognition.reasoner import Reasoner
from cognition.planner import Planner
from cognition.executor import Executor
from cognition.reflection import Reflection
from cognition.experience_engine import ExperienceEngine
from cognition.vision_engine import VisionEngine
from tools.voice_core import VoiceCore

class Orchestrator:
    """
    O AI CORE v4.0: Sistema de Operação Cognitiva Permanente.
    Implementa o Ciclo de 12 Etapas do CTO.
    """
    def __init__(self):
        self.voice = VoiceCore()
        self.memory = SOLPIMemory()
        self.world = WorldModel(self.memory)
        self.vision = VisionEngine()
        self.reasoner = Reasoner(self.memory)
        self.planner = Planner(self.memory)
        self.workflow = WorkflowEngine(self.planner, self.reasoner)
        self.experience = ExperienceEngine(self.memory)
        self.goal_manager = GoalManager(self.memory)
        self.executor = Executor(self.memory)
        self.reflection = Reflection(self.memory, self.voice)

    def solve(self, objective):
        start_time = time.time()
        errors = []
        
        # 1. COMPREENSÃO & VOZ
        self.voice.speak(f"Iniciando ciclo cognitivo para: {objective}")

        # 2. MODELO DE MUNDO (Sente o ambiente)
        current_world = self.world.update_state()

        # 3. PESQUISA DE MEMÓRIA & EXPERIÊNCIA
        lessons = self.experience.get_lesson_for(objective)

        # 4. PLANEJAMENTO (Task Tree)
        self.goal_manager.set_goal(objective)
        task_tree = self.workflow.generate_task_tree(objective, current_world)
        self.goal_manager.update_milestones(task_tree['branches'])

        # 5. RACIOCÍNIO & DECISÃO (Estratégias)
        strategy = self.reasoner.ponder(objective, lessons)

        # 6. EXECUÇÃO ORQUESTRADA
        execution_results = []
        for i, task in enumerate(task_tree['branches']):
            print(f"🚀 [AI CORE]: Executando nó {i+1} via {task['agent']}...")
            res = self.executor.run_plan([task])
            
            # 7. VERIFICAÇÃO (Vision/Reflection)
            valid = self.workflow.validate_step(res)
            if not valid:
                # 8. CORREÇÃO (Auto-Repair)
                self.voice.speak("Detectada inconsistência. Tentando rota de correção.")
                res = self.executor.run_plan([task]) # Retry simples por enquanto
                errors.append(f"Retry na etapa {i}")

            execution_results.append(res)
            self.goal_manager.mark_step_complete(i)

        # 9. DESTILAÇÃO DE APRENDIZADO
        duration = time.time() - start_time
        self.experience.distill({
            "problem": objective,
            "context": current_world,
            "tools_used": [t['agent'] for t in task_tree['branches']],
            "duration": duration,
            "result": str(execution_results),
            "errors": errors,
            "corrections": [],
            "confidence": strategy['score']
        })

        # 10. RESPOSTA FINAL
        success_msg = f"🏆 Objetivo concluído. {len(task_tree['branches'])} tarefas executadas em {duration:.2f}s."
        self.voice.speak(success_msg)
        return success_msg
