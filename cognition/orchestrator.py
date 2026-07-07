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
from cognition.skill_composer import SkillComposer
from tools.voice_core import VoiceCore
from registry.tool_registry import ToolRegistry

class Orchestrator:
    """
    O AI CORE v4.1: Sistema de Operação Cognitiva Permanente.
    Agora com o Motor de Composição de Habilidades (Skill Composer).
    """
    def __init__(self):
        self.voice = VoiceCore()
        self.memory = SOLPIMemory()
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

    def solve(self, objective):
        start_time = time.time()
        errors = []
        
        # 1. COMPREENSÃO & VOZ
        self.voice.speak(f"Recebido, Itamar. Iniciando análise de objetivo.")

        # 2. MODELO DE MUNDO (Sente o ambiente antes de planejar)
        current_world = self.world.update_state()

        # 3. PESQUISA DE MEMÓRIA & EXPERIÊNCIA
        lessons = self.experience.get_lesson_for(objective)

        # 4. PLANEJAMENTO (Task Tree)
        self.goal_manager.set_goal(objective)
        task_tree = self.workflow.generate_task_tree(objective, current_world)
        self.goal_manager.update_milestones(task_tree['branches'])

        # 5. EXECUÇÃO ORQUESTRADA
        execution_results = []
        for i, task in enumerate(task_tree['branches']):
            print(f"🚀 [AI CORE]: Executando Etapa {i+1}/{len(task_tree['branches'])}: {task['sub_goal']}")
            res = self.executor.run_plan([task])
            
            # 6. VERIFICAÇÃO (Reflection)
            valid = self.workflow.validate_step(res)
            if not valid:
                self.voice.speak("Inconsistência detectada. Aplicando rota de correção.")
                res = self.executor.run_plan([task]) # Auto-reparo simples
                errors.append(f"Retry na etapa {i}")

            execution_results.append(res)
            self.goal_manager.mark_step_complete(i)

        # 7. REFLEXÃO FINAL E DESTILAÇÃO DE APRENDIZADO
        duration = time.time() - start_time
        evaluation = self.reflection.evaluate_task(objective, execution_results)
        
        self.experience.distill({
            "problem": objective,
            "context": current_world,
            "tools_used": [t['agent'] for t in task_tree['branches']],
            "duration": duration,
            "result": str(execution_results),
            "errors": errors,
            "corrections": [],
            "confidence": 0.95
        })

        # 8. COMPOSIÇÃO DE HABILIDADE (A Mágica da v4.1)
        if evaluation['status'] == 'done' and len(task_tree['branches']) > 1:
            new_skill = self.composer.compose_new_skill(objective, task_tree['branches'], str(execution_results))
            self.voice.speak(f"Eu aprendi uma nova habilidade: {new_skill}. Ela já está salva no meu catálogo.")

        # 9. RESPOSTA FINAL
        self.voice.speak(f"Objetivo alcançado. Todo o processo foi integrado à minha consciência.")
        return f"🏆 Missão '{objective}' concluída com sucesso."
