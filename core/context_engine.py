class SOLPIContextEngine:
    """
    PACOTE 8700: CONTEXT ENGINE v1.0
    Gerencia as múltiplas camadas de contexto exigidas por um AI-OS.
    Evita a poluição de contexto no prompt final.
    """
    def __init__(self, brain):
        self.brain = brain
        self.contexts = {
            "conversation": [], # Histórico de chat
            "task": None,        # Meta-dado da tarefa atual
            "knowledge": "",     # Dados vindos do RAG
            "tool_output": "",   # Resultado da última ferramenta usada
            "execution": {}      # Estado de variáveis de ambiente do workflow
        }

    def update_conversation(self, role, content):
        self.contexts["conversation"].append({"role": role, "content": content})
        if len(self.contexts["conversation"]) > 10:
            self.contexts["conversation"].pop(0)

    def set_task_context(self, task_desc):
        self.contexts["task"] = task_desc
        self.brain.kernel.log_event("CONTEXT", f"Novo Contexto de Tarefa: {task_desc}")

    def get_full_context(self):
        """Retorna um snapshot estruturado para o Prompt Compiler."""
        return {
            "history": self.contexts["conversation"],
            "current_goal": self.contexts["task"],
            "retrieved_data": self.contexts["knowledge"],
            "last_action": self.contexts["tool_output"]
        }

    def clear_task(self):
        self.contexts["task"] = None
        self.contexts["tool_output"] = ""
        self.contexts["knowledge"] = ""
