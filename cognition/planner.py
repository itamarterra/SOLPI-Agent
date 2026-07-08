import re

class Planner:
    """
    O Planejador Universal do SOLPI OS v6.0.
    Agora capaz de delegar tarefas de alto desempenho para Hermes, Claude Code e OpenClaw.
    """
    def __init__(self, memory):
        self.memory = memory

    def create_plan(self, objective, world_context):
        print(f"📋 [PLANNER]: Decompondo objetivo universal...")
        plan = []
        obj_lower = objective.lower()
        
        # Função auxiliar para busca de palavras inteiras (evita 'ui' em 'pesquise')
        def has_word(word_list, text):
            for word in word_list:
                if re.search(rf'\b{word}\b', text):
                    return True
            return False

        # 1. Detecção de Especialidade de Engenharia (Salto para o Claude)
        if has_word(["revisão", "revise", "audit", "auditoria", "segurança", "arquitetura", "qualidade", "refat"], obj_lower):
             print("🧠 [PLANNER]: Detectada necessidade de engenharia. Delegando para ClaudeAgent.")
             plan.append({"id": 1, "task": objective, "agent": "ClaudeAgent"})
             return plan

        # 2. Detecção de Especialidade de Interface/Mensagem (Salto para o OpenClaw)
        if has_word(["ui", "botão", "clique", "menu", "whatsapp", "telegram", "mensagem", "notifica", "notificação"], obj_lower):
             print("🦾 [PLANNER]: Detectada necessidade de automação de UI/Mensagem. Delegando para OpenClawAgent.")
             plan.append({"id": 1, "task": objective, "agent": "OpenClawAgent"})
             return plan

        # 3. Detecção de Complexidade Operacional (Salto para o Hermes)
        if len(obj_lower.split()) > 15 or has_word(["instale", "configure", "projeto", "migre", "setup", "servidor"], obj_lower):
             print("🏛️ [PLANNER]: Detectada alta complexidade operacional. Delegando para HermesAgent.")
             plan.append({"id": 1, "task": objective, "agent": "HermesAgent"})
             return plan

        # 4. Sequência de Ações Tradicional
        if "abra" in obj_lower and "pesquise" in obj_lower:
            parts = obj_lower.split(" e ")
            for i, part in enumerate(parts):
                if any(x in part for x in ["site", "youtube", "google", "pesquise"]):
                    plan.append({"id": i+1, "task": part, "agent": "BrowserAgent"})
                else:
                    plan.append({"id": i+1, "task": part, "agent": "AutomationAgent"})

        elif has_word(["clique", "digite", "tela"], obj_lower):
            plan.append({"id": 1, "task": objective, "agent": "AutomationAgent"})

        elif obj_lower.startswith("$ ") or has_word(["shell", "terminal"], obj_lower):
            plan.append({"id": 1, "task": objective, "agent": "WindowsAgent"})

        # 4. LIBERTAÇÃO SEMÂNTICA (IA pura decide se não houver regra fixa)
        else:
            print("🧠 [PLANNER]: Nenhuma regra fixa detectada. Usando Raciocínio de Elite para delegar...")
            # Delega para o ProgrammingAgent como mestre de lógica se houver dúvida
            plan.append({"id": 1, "task": objective, "agent": "ProgrammingAgent"})
            
        print(f"✅ [PLANNER]: Plano multitarefa com {len(plan)} etapas gerado.")
        return plan
