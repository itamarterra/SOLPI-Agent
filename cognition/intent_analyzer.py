class IntentAnalyzer:
    def __init__(self, llm_engine):
        self.llm = llm_engine

    def analyze(self, user_input, world_state):
        ui = user_input.lower()
        
        # Filtro de Regras Local (Garante que conversa simples não vire 'Missão')
        if any(greet in ui for key, greet in [("oi", "oi"), ("ola", "olá"), ("boa noite", "boa noite"), ("bom dia", "bom dia")]):
            return "CONVERSATION"

        prompt = f"""
        Classifique a intenção do usuário: "{user_input}"
        Responda APENAS: CONVERSATION ou GOAL.
        """
        messages = [{"role": "user", "content": prompt}]
        res = self.llm.chat(messages)
        
        try:
            content = res['choices'][0]['message']['content'].upper()
            if "GOAL" in content: return "GOAL"
            return "CONVERSATION"
        except:
            return "CONVERSATION"
