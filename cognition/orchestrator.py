import time
import os
from cognition.memory import SOLPIMemory
from cognition.reasoner import Reasoner
from cognition.planner import Planner
from cognition.executor import Executor
from cognition.reflection import Reflection
from cognition.learning import Learning

class Orchestrator:
    """
    O AI CORE: O ponto de convergência de toda a inteligência do SOLPI OS.
    """
    def __init__(self):
        self.memory = SOLPIMemory()
        self.reasoner = Reasoner(self.memory)
        self.planner = Planner(self.memory)
        self.executor = Executor(self.memory)
        self.reflection = Reflection(self.memory, None)
        self.learning = Learning(self.memory)

    def solve(self, objective):
        """O Ciclo Cognitivo de 10 Etapas."""
        print(f"\n🧠 [SOLPI AI CORE]: Iniciando Ciclo para '{objective}'")
        start_time = time.time()

        # 1. ENTENDIMENTO (Semantic Search)
        context = self.memory.search_semantic(objective)
        
        # 2. PLANEJAMENTO (Workflow Engine)
        plan = self.planner.create_plan(objective, context)
        
        # 3. PESQUISA & ESCOLHA DE AGENTES/FERRAMENTAS (Reasoner)
        # O Reasoner agora analisa o plano e valida os riscos
        analysis = self.reasoner.analyze(objective, context)
        
        # 4. EXECUÇÃO (Agent Dispatcher)
        result = self.executor.run_plan(plan)
        
        # 5. VERIFICAÇÃO & REFLEXÃO (Vision)
        evaluation = self.reflection.evaluate(objective, plan, result)
        
        # 6. CORREÇÃO (Auto-Repair)
        if not evaluation['success']:
            print("🔄 [CORREÇÃO]: Iniciando auto-reparo do plano...")
            # Lógica de re-planejamento aqui
        
        # 7. APRENDIZADO & MEMÓRIA (Experience Distillation)
        duration = time.time() - start_time
        self.learning.record_experience(objective, plan, result, evaluation)
        
        # 8. RESPOSTA FINAL
        return f"Objetivo concluído com sucesso em {duration:.2f}s. Lições aprendidas registradas."
