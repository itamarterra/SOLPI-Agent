class WorkflowEngine:
    """
    O Motor de Decomposição e Cadeia de Tarefas (Task Tree).
    Transforma intenções em grafos de execução lógicos.
    """
    def __init__(self, planner, reasoner):
        self.planner = planner
        self.reasoner = reasoner

    def generate_task_tree(self, objective, world_context):
        """Cria uma estrutura hierárquica de objetivos e subtarefas."""
        print(f"🌲 [WORKFLOW]: Gerando Task Tree para: {objective}")
        
        # O Planner gera o plano base
        base_plan = self.planner.create_plan(objective, world_context)
        
        task_tree = {
            "root_goal": objective,
            "branches": []
        }

        for step in base_plan:
            # Para cada passo, o Reasoner valida a estratégia
            strategy = self.reasoner.ponder(step['task'], world_context)
            
            branch = {
                "id": step['id'],
                "sub_goal": step['task'],
                "agent": step['agent'],
                "strategy": strategy['name'],
                "status": "pending",
                "validation_required": True
            }
            task_tree["branches"].append(branch)
            
        return task_tree

    def validate_step(self, step_result):
        """Verifica se o nó da árvore foi concluído com sucesso."""
        return "error" not in str(step_result).lower()
