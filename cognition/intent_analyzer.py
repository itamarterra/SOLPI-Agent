class IntentAnalyzer:
    def __init__(self, llm_engine):
        self.llm = llm_engine

    def analyze(self, user_input, world_state):
        ui = user_input.lower()
        
        # Vocabulário Estendido de Conversa (Manual para evitar chamadas de API caras/lentas)
        conversational_phrases = [
            "oi", "ola", "olá", "bom dia", "boa tarde", "boa noite", 
            "tudo bem", "como voce esta", "como vai", "quem e voce", 
            "o que voce faz", "obrigado", "valeu", "tchau", "adeus",
            "clima", "tempo", "voce e real", "inteligente"
        ]

        if any(phrase in ui for phrase in conversational_phrases):
            return "CONVERSATION"

        # Se não for uma saudação óbvia, tenta o LLM
        prompt = f"""
        Classifique a intenção do usuário: "{user_input}"
        Considere se o usuário quer apenas conversar ou se quer que eu execute uma tarefa técnica.
        Categorias:
        - CONVERSATION: Papo furado, perguntas sobre o eu, saudações, curiosidades.
        - GOAL: Comandos para o PC, automação, busca de produtos, análise de sistemas.
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
