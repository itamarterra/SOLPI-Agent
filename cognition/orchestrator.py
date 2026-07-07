import time
import os
from cognition.memory import SOLPIMemory
from cognition.reasoner import Reasoner
from cognition.planner import Planner
from cognition.executor import Executor
from cognition.reflection import Reflection
from cognition.learning import Learning
from cognition.decision import DecisionMaker
from cognition.knowledge import KnowledgeManager
from registry.tool_registry import ToolRegistry

class Orchestrator:
    """
    O Maestro Supremo do SOLPI OS.
    Controla o ciclo de Autonomia Cognitiva.
    """
    def __init__(self):
        self.memory = SOLPIMemory()
        self.knowledge = KnowledgeManager(self.memory)
        self.reasoner = Reasoner(self.memory)
        self.planner = Planner(self.memory)
        self.decision = DecisionMaker(self.memory)
        self.executor = Executor(self.memory)
        self.reflection = Reflection(self.memory, None)
        self.learning = Learning(self.memory)
        self.registry = ToolRegistry()
        self.monitor = None # Injetado pelo Kernel

    def solve(self, objective):
        """
        Entender -> Planejar -> Raciocinar -> Executar -> Verificar -> Aprender
        """
        start_time = time.time()
        print(f"\n🎯 [OBJETIVO]: {objective}")
        
        # 1. CONTEXTO
        past_memories = self.memory.search(objective)
        
        # 2. PLANEJAMENTO
        plan = self.planner.create_plan(objective, {"context": past_memories})
        
        # 3. RACIOCÍNIO & RISCO
        for step in plan:
            analysis = self.reasoner.analyze(step['task'], past_memories)
            step['strategy'] = analysis['strategy']

        # 4. EXECUÇÃO
        result = self.executor.run_plan(plan)
        
        # 5. REFLEXÃO
        evaluation = self.reflection.evaluate(objective, plan, result)
        
        # 6. TELEMETRIA & APRENDIZADO
        duration = time.time() - start_time
        if self.monitor:
            self.monitor.log_metric("Orchestrator", duration, evaluation['success'])
            
        self.learning.record_experience(objective, plan, result, evaluation)
        
        return result
