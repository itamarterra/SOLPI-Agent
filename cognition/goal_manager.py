class GoalManager:
    """
    O Gestor de Intenções do SOLPI OS.
    Transforma um desejo do usuário em uma meta persistente.
    """
    def __init__(self, memory):
        self.memory = memory
        self.active_goal = None

    def set_goal(self, objective):
        self.active_goal = {
            "objective": objective,
            "status": "thinking",
            "milestones": [],
            "current_step": 0
        }
        print(f"🎯 [GOAL]: Novo objetivo estratégico definido: {objective}")

    def update_milestones(self, plan):
        """Converte o plano em marcos de conclusão."""
        if not self.active_goal: return
        self.active_goal["milestones"] = plan
        self.active_goal["status"] = "executing"

    def mark_step_complete(self, step_id):
        if not self.active_goal: return
        self.active_goal["current_step"] = step_id
        if step_id == len(self.active_goal["milestones"]) - 1:
            self.active_goal["status"] = "achieved"

    def get_status(self):
        return self.active_goal
