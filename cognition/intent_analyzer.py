class IntentAnalyzer:
    """
    Classifica a intenção do usuário usando o LLM.
    """
    def __init__(self, llm_engine):
        self.llm = llm_engine

    def analyze(self, user_input, world_state):
        prompt = f"""
        Analise a mensagem do usuário e o estado do sistema.
        Estado: {world_state}
        Mensagem: "{user_input}"
        
        Classifique em uma destas categorias:
        - CONVERSATION: Apenas bate-papo.
        - GOAL: Pedido para executar uma tarefa no PC ou Web.
        - QUESTION: Pergunta sobre dados ou sistema.
        - TROUBLESHOOTING: Pedido para resolver um erro detectado.

        Responda apenas com o nome da categoria em MAIÚSCULAS.
        """
        
        messages = [{"role": "system", "content": "Você é o Intent Analyzer do SOLPI OS."},
                    {"role": "user", "content": prompt}]
        
        res = self.llm.chat(messages)
        try:
            return res['choices'][0]['message']['content'].strip()
        except:
            return "CONVERSATION"
