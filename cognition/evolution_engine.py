import os
from agents.programming_agent import ProgrammingAgent

class EvolutionEngine:
    """
    O Motor de Auto-Aperfeiçoamento do SOLPI OS.
    Utiliza o ProgrammingAgent para modificar o próprio sistema baseado em experiências.
    """
    def __init__(self, memory, registry):
        self.memory = memory
        self.registry = registry
        self.engineer = ProgrammingAgent(memory)

    def evolve_system(self, feedback):
        """
        Analisa o feedback da Reflection e decide se deve criar uma nova Skill ou 
        melhorar um Agente existente.
        """
        print(f"🧬 [EVOLUTION]: Analisando feedback para auto-melhoria...")
        
        # Se o feedback indica uma falha recorrente em uma ferramenta
        if "falha" in feedback.lower():
            self.engineer.execute("valide o código do core para encontrar bugs")
            return "🔧 Auto-diagnóstico de engenharia concluído."
            
        # Se for uma nova tarefa bem-sucedida, transforma em 'Procedural Memory' (Skill)
        return "🧬 Sistema em estado de equilíbrio. Nenhuma evolução necessária no momento."

    def create_dynamic_skill(self, name, description, steps):
        """Cria uma nova habilidade (.md) e a registra no sistema dinamicamente."""
        skill_content = f"""---
name: {name}
description: "{description}"
---
# {name}
{steps}
"""
        path = f"skills/{name}/SKILL.md"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        
        print(f"✨ [MARKETPLACE]: Nova Skill '{name}' gerada e instalada localmente.")
        return path
