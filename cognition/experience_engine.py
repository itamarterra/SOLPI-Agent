import json
from datetime import datetime

class ExperienceEngine:
    """
    O Coração do Aprendizado do SOLPI OS v4.0.
    Transforma execuções passadas em sabedoria procedimental.
    """
    def __init__(self, memory):
        self.memory = memory

    def distill(self, execution_data):
        """
        Registra uma experiência completa para reutilização futura.
        execution_data: {
            'problem': str,
            'context': dict,
            'tools_used': list,
            'duration': float,
            'result': str,
            'errors': list,
            'corrections': list,
            'confidence': float
        }
        """
        print("🧬 [EXPERIENCE]: Destilando nova experiência...")
        
        experience_entry = {
            "timestamp": datetime.now().isoformat(),
            "data": execution_data,
            "best_solution": execution_data['result'] if not execution_data['errors'] else "RETRY_REQUIRED"
        }
        
        # Armazena na camada de experiência da memória
        self.memory.store(
            content=json.dumps(experience_entry, ensure_ascii=False),
            layer="experience",
            tags=f"skill_learning,{execution_data['problem'][:20]}"
        )
        
        return "Experiência integrada ao Cérebro."

    def get_lesson_for(self, objective):
        """Consulta experiências passadas para o mesmo objetivo."""
        past = self.memory.search(objective, layer="experience")
        if past:
            print(f"💡 [EXPERIENCE]: Encontrei {len(past)} lições aprendidas para este objetivo.")
            return past
        return None
