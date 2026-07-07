import json
from datetime import datetime

class Learning:
    """
    O Motor de Evolução do SOLPI-AIOS.
    Extrai lições, boas práticas e otimiza o conhecimento do sistema após cada tarefa.
    """
    def __init__(self, memory):
        self.memory = memory

    def record_experience(self, objective, plan, result, evaluation):
        print(f"🧬 [LEARNING]: Destilando experiência para o futuro...")
        
        experience_data = {
            "objective": objective,
            "best_steps": plan,
            "outcome": "POSITIVE" if evaluation["success"] else "NEGATIVE",
            "learned_at": datetime.now().isoformat()
        }
        
        # Salva na camada de Experiência da Memória
        self.memory.remember(
            content=json.dumps(experience_data, ensure_ascii=False),
            layer="experience",
            tags=f"learning,{evaluation['success']}"
        )
        
        # Se falhou, registra como um "Erro Conhecido" para o Reasoner evitar no futuro
        if not evaluation["success"]:
            self.memory.remember(
                content=f"Falha ao tentar: {objective}. Causa: {evaluation['feedback']}",
                layer="knowledge",
                tags="failure_case"
            )
            
        return "Conhecimento atualizado."
