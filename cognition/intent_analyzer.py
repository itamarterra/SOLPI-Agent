class IntentAnalyzer:
    def __init__(self, llm_engine):
        self.llm = llm_engine

    def analyze(self, user_input, world_state):
        ui = user_input.lower()
        
        # Palavras de Ação Imediata (Forçam GOAL)
        action_keywords = [
            "abra", "pesquise", "busque", "crie", "delete", "configure", 
            "instale", "rode", "execute", "verifique", "revise", "audite",
            "notifique", "mande", "clique", "digite", "scan"
        ]

        if any(word in ui for word in action_keywords):
            return "GOAL"

        # Vocabulário Estendido de Conversa
        conversational_phrases = [
            "oi", "ola", "olá", "bom dia", "boa tarde", "boa noite", 
            "tudo bem", "como voce esta", "como vai", "quem e voce", 
            "o que voce faz", "obrigado", "valeu", "tchau", "adeus"
        ]

        if any(phrase in ui for phrase in conversational_phrases):
            return "CONVERSATION"

        # Se não for uma saudação óbvia, tenta o LLM usando o DNA do Trinity
        prompt = f"""
        Você é o Kernel do SOLPI OS. Analise a ordem do Comandante Itamar: "{user_input}"
        
        Sua tarefa é classificar se ele quer conversar/perguntar algo (CONVERSATION) ou se ele quer que você realize uma ação técnica/operação (GOAL).

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
