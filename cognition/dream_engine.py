import json
import os
from datetime import datetime

class DreamEngine:
    """
    O Motor de Evolução Autônoma v6.0.
    Processa experiências passadas (Sonhos) para gerar novas capacidades.
    Permite que o SOLPI OS aprenda com o erro e se torne 'mais livre'.
    """
    def __init__(self, memory, registry):
        self.memory = memory
        self.registry = registry
        self.traces_path = "logs/mesh_traces.jsonl"

    def synthesize_experience(self):
        """Analisa os rastros da malha e gera novos conhecimentos."""
        print("🧠 [DREAM ENGINE]: Iniciando ciclo de síntese neural...")
        
        if not os.path.exists(self.traces_path):
            return "Nenhum rastro encontrado para processamento."

        with open(self.traces_path, "r", encoding="utf-8") as f:
            traces = [json.loads(line) for line in f]

        # 1. Identifica falhas recorrentes para sugerir auto-reparos
        failures = [t for t in traces if t['status'] == 'failed']
        
        # 2. Identifica sucessos para 'Solidificar' como novas habilidades
        successes = [t for t in traces if t['status'] == 'completed']

        if successes:
            new_skill = self._distill_skill(successes[-1])
            return f"Evolução concluída. Nova habilidade destilada: {new_skill}"
        
        return "Ciclo de sonho concluído. Estabilidade mantida."

    def _distill_skill(self, last_success):
        """Transforma um sucesso isolado em uma SKILL permanente."""
        skill_name = f"auto-{last_success['agent'].lower()}-{datetime.now().strftime('%M%S')}"
        skill_path = f"skills/{skill_name}"
        os.makedirs(skill_path, exist_ok=True)
        
        with open(f"{skill_path}/SKILL.md", "w", encoding="utf-8") as f:
            f.write(f"# 🦾 Habilidade Auto-Gerada: {skill_name}\n")
            f.write(f"Destilada do rastro de sucesso do {last_success['agent']}.\n")
            f.write(f"Tarefa executada: {last_success['task']}\n")
            f.write(f"Data de Nascimento: {datetime.now().isoformat()}\n")
            
        print(f"📦 [EVOLUTION]: O sistema se libertou de uma dependência manual. Nova Skill: {skill_name}")
        return skill_name
