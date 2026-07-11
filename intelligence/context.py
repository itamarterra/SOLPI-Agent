class SOLPIContextEngine:
    """
    PACOTE 8700: CONTEXT ENGINE v50.0
    Organizador semântico de memória de trabalho.
    """
    def __init__(self, brain):
        self.brain = brain
        self.contexts = {
            "conversation": [],
            "task": None,
            "knowledge": "",
            "tool_output": "",
            "execution": {}
        }

    def update_conversation(self, role, content):
        self.contexts["conversation"].append({"role": role, "content": content})
        if len(self.contexts["conversation"]) > 10: self.contexts["conversation"].pop(0)

    def set_task_context(self, task_desc):
        self.contexts["task"] = task_desc
        self.brain.kernel.log_event("CONTEXT", f"Ativando foco em: {task_desc}")

    def get_full_context(self):
        return {
            "history": self.contexts["conversation"],
            "current_goal": self.contexts["task"],
            "retrieved_data": self.contexts["knowledge"],
            "last_action": self.contexts["tool_output"]
        }
