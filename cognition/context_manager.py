from datetime import datetime

class ContextManager:
    """
    Mantém a coerência operacional do SOLPI OS.
    Rastreia o objetivo atual, prioridades e estado do ambiente.
    """
    def __init__(self):
        self.current_context = {
            "active_goal": None,
            "priority": "normal",
            "history": [],
            "active_agents": [],
            "environment_state": {},
            "start_time": None
        }

    def update_environment(self, world_state):
        self.current_context["environment_state"] = world_state

    def set_goal(self, objective, priority="normal"):
        self.current_context["active_goal"] = objective
        self.current_context["priority"] = priority
        self.current_context["start_time"] = datetime.now()
        self.current_context["history"].append(f"Goal set: {objective}")

    def log_action(self, agent, tool, result):
        entry = {
            "time": datetime.now().isoformat(),
            "agent": agent,
            "tool": tool,
            "success": "error" not in str(result).lower()
        }
        self.current_context["history"].append(entry)

    def get_snapshot(self):
        return self.current_context
