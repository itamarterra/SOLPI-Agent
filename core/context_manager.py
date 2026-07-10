class SOLPIContextManager:
    """
    PACOTE 1307: CONTEXT MANAGER v1.0
    Gerencia a janela de contexto para garantir coerência.
    """
    def __init__(self, max_tokens=1024):
        self.max_tokens = max_tokens
        self.history = []

    def add_to_context(self, role, content):
        self.history.append({"role": role, "content": content})
        # Mantém apenas as últimas 10 interações (Janela deslizante)
        if len(self.history) > 10:
            self.history.pop(0)

    def get_full_prompt(self):
        """Constrói o prompt final com base no histórico."""
        full_text = ""
        for entry in self.history:
            full_text += f"{entry['role'].upper()}: {entry['content']}\n"
        return full_text
