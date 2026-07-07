import time
import os

class Reflection:
    """
    O Crítico do SOLPI-AIOS.
    Avalia se as ações executadas pelos agentes atingiram o objetivo esperado.
    """
    def __init__(self, memory, tools):
        self.memory = memory
        self.tools = tools

    def evaluate(self, objective, plan, result):
        print(f"🧐 [REFLECTION]: Avaliando eficácia da execução...")
        
        # 1. Análise de Sucesso (Baseado em texto por enquanto)
        success = True
        feedback = "Objetivo parece ter sido alcançado."
        
        if "erro" in str(result).lower() or "falha" in str(result).lower():
            success = False
            feedback = "A execução encontrou erros técnicos."
        
        # 2. Verificação Sensorial (Simulada)
        # Em tarefas de UI, poderíamos tirar um print e comparar com o esperado
        
        print(f"⚖️ [REFLECTION]: Resultado -> {'Sucesso' if success else 'Falha'}. Feedback: {feedback}")
        
        return {
            "success": success,
            "feedback": feedback,
            "performance_score": 0.9 if success else 0.2
        }

    def should_retry(self, evaluation):
        """Decide se o Orquestrador deve tentar novamente ou pedir ajuda."""
        return not evaluation["success"]
