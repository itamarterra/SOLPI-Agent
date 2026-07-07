import time
import os
from cognition.memory import SOLPIMemory
from cognition.reasoner import Reasoner
from cognition.planner import Planner
from cognition.executor import Executor
from cognition.reflection import Reflection
from cognition.learning import Learning
from core.tools import AgentTools

class Orchestrator:
    """
    O Maestro Supremo do SOLPI-AIOS.
    Gerencia o ciclo de vida cognitivo completo.
    """
    def __init__(self):
        self.memory = SOLPIMemory()
        self.tools = AgentTools()
        self.reasoner = Reasoner(self.memory)
        self.planner = Planner(self.memory)
        self.executor = Executor(self.memory)
        self.reflection = Reflection(self.memory, self.tools)
        self.learning = Learning(self.memory)
        print("🧠 [ORCHESTRATOR]: Sistema Operacional Cognitivo SOLPI-AIOS Ativo.")

    def solve(self, objective):
        """
        Ciclo Cognitivo Universal:
        Entender -> Planejar -> Executar -> Verificar -> Aprender -> Evoluir
        """
        start_time = time.time()
        print(f"\n🎯 [OBJETIVO]: {objective}")
        
        # 1. ENTENDER & RACIOCINAR
        context = self.memory.recall(objective)
        analysis = self.reasoner.analyze(objective, context)
        
        # 2. PLANEJAR
        plan = self.planner.create_plan(objective, analysis)
        
        # 3. VERIFICAR LÓGICA DO PLANO
        valid, msg = self.reasoner.verify_logic(plan)
        if not valid:
            return f"❌ Abortado pelo Reasoner: {msg}"
        
        # 4. EXECUTAR (Delegação aos Multi-Agentes)
        result = self.executor.run_plan(plan)
        
        # 5. REFLETIR (Avaliação de Resultado)
        evaluation = self.reflection.evaluate(objective, plan, result)
        
        # 6. TENTAR CORREÇÃO SE FALHAR (Auto-Reparo)
        if self.reflection.should_retry(evaluation):
            print("🔄 [ORCHESTRATOR]: Detectada falha. Tentando estratégia de correção...")
            # Futuramente: solicitar novo plano ao Planner focado no erro
        
        # 7. APRENDER (Registro de Experiência)
        duration = time.time() - start_time
        self.learning.record_experience(objective, plan, result, evaluation)
        self.memory.log_task(objective, str(plan), result, "SUCCESS" if evaluation["success"] else "FAILED", duration)
        
        print(f"🏁 [CICLO CONCLUÍDO]: {duration:.2f}s")
        return result
