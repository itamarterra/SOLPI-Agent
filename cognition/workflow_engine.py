class WorkflowEngine:
    def __init__(self, planner, reasoner):
        self.planner = planner
        self.reasoner = reasoner

    def generate_task_tree(self, objective, world_context):
        print(f"🌲 [WORKFLOW]: Gerando Task Tree para: {objective}")
        base_plan = self.planner.create_plan(objective, world_context)
        
        task_tree = {"root_goal": objective, "branches": []}

        for step in base_plan:
            # O Reasoner retorna 'strategy' (string), não um objeto com 'name'
            strategy_info = self.reasoner.ponder(step['task'], world_context)
            
            branch = {
                "id": step['id'],
                "sub_goal": step['task'],
                "agent": step['agent'],
                "strategy": strategy_info.get('strategy', 'Default'),
                "status": "pending"
            }
            task_tree["branches"].append(branch)
            
        return task_tree

    def validate_step(self, step_result):
        return "error" not in str(step_result).lower()
