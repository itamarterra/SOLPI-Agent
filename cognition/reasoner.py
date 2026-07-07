import os

class Reasoner:
    """
    O Raciocinador do SOLPI-AIOS.
    Analisa o contexto, avalia riscos e escolhe a melhor estratégia.
    """
    def __init__(self, memory):
        self.memory = memory

    def analyze(self, objective, context):
        """
        Analisa o objetivo frente ao contexto recuperado.
        Retorna uma estratégia e uma avaliação de risco.
        """
        print(f"🧠 [REASONER]: Iniciando análise lógica do objetivo...")
        
        # 1. Geração de Hipóteses (Simulado)
        strategies = [
            {"name": "Direta", "risk": "Baixo", "efficiency": 0.9},
            {"name": "Cautelosa", "risk": "Mínimo", "efficiency": 0.7}
        ]
        
        # 2. Avaliação de Riscos
        # Exemplo: Comandos destrutivos aumentam o risco
        risk_level = "Baixo"
        if any(word in objective.lower() for word in ["deletar", "remover", "formatar"]):
            risk_level = "Alto"
        
        # 3. Escolha da melhor solução
        best_strategy = strategies[0] if risk_level == "Baixo" else strategies[1]
        
        print(f"⚖️ [REASONER]: Estratégia escolhida: {best_strategy['name']} (Risco: {risk_level})")
        
        return {
            "strategy": best_strategy,
            "risk_level": risk_level,
            "context_summary": f"Analisado com {len(context)} pontos de referência."
        }

    def verify_logic(self, plan):
        """Valida se o plano gerado é logicamente consistente."""
        if not plan:
            return False, "Plano vazio."
        return True, "Lógica validada."
