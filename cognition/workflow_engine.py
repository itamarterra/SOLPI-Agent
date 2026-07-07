class WorkflowEngine:
    """
    O Motor de Decomposição do SOLPI OS.
    Quebra objetivos em subtarefas atômicas e lógicas.
    """
    def __init__(self, planner):
        self.planner = planner

    def decompose(self, objective, context):
        """Transforma um objetivo 'preparar servidor' em passos reais."""
        print(f"⚙️ [WORKFLOW]: Decompondo objetivo complexo...")
        
        # O motor de fluxo usa o Planner e o Reasoner para criar a sequência
        # Aqui injetaremos lógica de grafos de dependência no futuro
        plan = self.planner.create_plan(objective, context)
        
        # Adiciona validação de pré-requisitos para cada passo
        for step in plan:
            step["verified"] = False
            
        return plan
