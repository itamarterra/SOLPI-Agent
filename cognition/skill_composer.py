import os
import json
from datetime import datetime

class SkillComposer:
    """
    O COMPOSITOR DE HABILIDADES do SOLPI OS.
    Analisa execuções bem-sucedidas e as transforma em novas 'Skills' permanentes.
    Inspirado no conceito de 'Self-Improving Learning Loop'.
    """
    def __init__(self, memory, registry):
        self.memory = memory
        self.registry = registry
        self.skills_dir = "skills"

    def compose_new_skill(self, objective, execution_steps, result_summary):
        """
        Transforma uma sequência de tarefas em um manual reutilizável.
        """
        print(f"✨ [COMPOSER]: Sintetizando nova habilidade baseada em '{objective}'...")
        
        # 1. Gera o nome técnico da skill (slug)
        skill_name = objective.lower().replace(" ", "-")[:30].strip("-")
        
        # 2. Constrói o corpo da Skill (Markdown padrão OpenClaw)
        steps_md = "\n".join([f"{i+1}. {step['task']} (via {step['agent']})" for i, step in enumerate(execution_steps)])
        
        skill_content = f"""---
name: {skill_name}
description: "Habilidade composta para: {objective}"
version: "1.0.0"
created_at: "{datetime.now().isoformat()}"
---

# {objective.title()}

Esta habilidade foi aprendida autonomamente pelo SOLPI OS após uma execução bem-sucedida.

## Fluxo de Trabalho Original
{steps_md}

## Resultado Esperado
{result_summary}

## Notas de Experiência
- Executada em {datetime.now().strftime('%d/%m/%Y')}
- Validada por: Reflection Engine
"""
        
        # 3. Salva fisicamente o novo conhecimento
        skill_path = os.path.join(self.skills_dir, skill_name)
        os.makedirs(skill_path, exist_ok=True)
        file_path = os.path.join(skill_path, "SKILL.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
            
        # 4. Registra na Memória Procedural
        self.memory.store(
            content=f"Nova Skill aprendida: {skill_name}. Capacidade: {objective}",
            layer="knowledge",
            tags="new_skill,procedural"
        )
        
        print(f"✅ [COMPOSER]: Skill '{skill_name}' forjada e salva em {file_path}")
        return skill_name
