class Planner:
    """
    O Planejador Universal do SOLPI-AIOS.
    Distribui tarefas entre PC (Windows), Web (Browser) e Interface (Automation).
    """
    def __init__(self, memory):
        self.memory = memory

    def create_plan(self, objective, analysis):
        print(f"📋 [PLANNER]: Decompondo objetivo universal...")
        plan = []
        obj_lower = objective.lower()
        
        # 1. Identificação de Sequência de Ações (O coração da autonomia)
        
        # Ex: "Abra o youtube e pesquise por musica"
        if "abra" in obj_lower and "pesquise" in obj_lower:
            parts = obj_lower.split(" e ")
            for i, part in enumerate(parts):
                if "site" in part or "youtube" in part or "google" in part:
                    plan.append({"id": i+1, "task": part, "agent": "BrowserAgent"})
                elif "pesquise" in part:
                    plan.append({"id": i+1, "task": part, "agent": "BrowserAgent"})
                elif "clique" in part or "digite" in part:
                    plan.append({"id": i+1, "task": part, "agent": "AutomationAgent"})

        # Ex: Comandos de Interface Direta (Clique, Digite, etc)
        elif any(x in obj_lower for x in ["clique", "digite", "pressione", "aperte", "tela", "print"]):
            plan.append({"id": 1, "task": objective, "agent": "AutomationAgent"})

        # Ex: Comandos Web Diretos
        elif any(x in obj_lower for x in ["site", "youtube", "google", "internet", "nuvem"]):
            plan.append({"id": 1, "task": objective, "agent": "BrowserAgent"})

        # Ex: Comandos de Sistema ($ ou shell)
        elif any(x in obj_lower for x in ["pasta", "arquivo", "$", "comando", "sistema", "diretório"]):
            plan.append({"id": 1, "task": objective, "agent": "WindowsAgent"})

        else:
            # Se for incerto, o AutomationAgent tenta localizar e agir
            plan.append({"id": 1, "task": objective, "agent": "AutomationAgent"})
            
        print(f"✅ [PLANNER]: Plano multitarefa com {len(plan)} etapas gerado.")
        return plan
