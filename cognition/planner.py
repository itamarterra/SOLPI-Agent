class Planner:
    """
    O Planejador Universal do SOLPI OS v6.0.
    Agora capaz de delegar tarefas de alto desempenho para Hermes e Claude Code.
    """
    def __init__(self, memory):
        self.memory = memory

    def create_plan(self, objective, world_context):
        print(f"📋 [PLANNER]: Decompondo objetivo universal...")
        plan = []
        obj_lower = objective.lower()
        
        # 1. Detecção de Especialidade de Engenharia (Salto para o Claude)
        if any(x in obj_lower for x in ["revis", "audit", "segurança", "arquitetura", "qualidade", "refat"]):
             print("🧠 [PLANNER]: Detectada necessidade de engenharia. Delegando para ClaudeAgent.")
             plan.append({"id": 1, "task": objective, "agent": "ClaudeAgent"})
             return plan

        # 2. Detecção de Complexidade Operacional (Salto para o Hermes)
        if len(obj_lower.split()) > 10 or any(x in obj_lower for x in ["instale", "configure", "projeto", "migre", "setup"]):
             print("🏛️ [PLANNER]: Detectada alta complexidade operacional. Delegando para HermesAgent.")
             plan.append({"id": 1, "task": objective, "agent": "HermesAgent"})
             return plan

        # 3. Sequência de Ações Tradicional
        if "abra" in obj_lower and "pesquise" in obj_lower:
            parts = obj_lower.split(" e ")
            for i, part in enumerate(parts):
                if any(x in part for x in ["site", "youtube", "google"]):
                    plan.append({"id": i+1, "task": part, "agent": "BrowserAgent"})
                else:
                    plan.append({"id": i+1, "task": part, "agent": "AutomationAgent"})

        elif any(x in obj_lower for x in ["clique", "digite", "tela"]):
            plan.append({"id": 1, "task": objective, "agent": "AutomationAgent"})

        elif any(x in obj_lower for x in ["$ ", "shell ", "terminal"]):
            plan.append({"id": 1, "task": objective, "agent": "WindowsAgent"})

        else:
            plan.append({"id": 1, "task": objective, "agent": "ProgrammingAgent"})
            
        print(f"✅ [PLANNER]: Plano multitarefa com {len(plan)} etapas gerado.")
        return plan
