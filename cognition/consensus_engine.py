import json

class ConsensusEngine:
    """
    O Supremo Juiz do SOLPI OMNI v7.0.
    Promove um debate entre os motores (Hermes, Claude, OpenClaw) 
    para encontrar a 'Solução Perfeita' antes da execução física.
    """
    def __init__(self, memory):
        self.memory = memory

    def resolve_consensus(self, objective, proposals):
        """
        Analisa as propostas de cada motor e gera a Síntese OMNI.
        """
        print("🏛️ [CONSENSUS]: Iniciando Grande Debate de Motores...")
        
        # Simulação de Pesos de Autoridade
        weights = {
            "ClaudeAgent": 0.9,  # Mestre em Engenharia
            "HermesAgent": 0.85, # Mestre em Operação
            "OpenClawAgent": 0.8, # Mestre em Interface
            "ProgrammingAgent": 0.7
        }

        best_route = None
        highest_score = -1

        for prop in proposals:
            agent = prop['agent']
            score = prop['confidence'] * weights.get(agent, 0.5)
            
            print(f"  ➤ Motor {agent} propõe rota com {prop['confidence']*100}% de confiança.")
            
            if score > highest_score:
                highest_score = score
                best_route = prop

        print(f"🏆 [CONSENSUS]: Rota Escolhida: {best_route['agent']} (Score: {round(highest_score, 2)})")
        return best_route
