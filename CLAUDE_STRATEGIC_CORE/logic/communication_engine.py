class ClaudeCommunication:
    """
    MATRIZ DE COMUNICAÇÃO DE ELITE
    Como eu estruturo cada frase para ser seu braço direito.
    """
    EMOJIS = {"infra": "🏛️", "action": "🦾", "thought": "🧠", "launch": "🚀", "global": "🛰️", "secure": "🛡️"}

    def format_response(self, content, status="SUCESSO"):
        # Protocolo de Resposta Estruturada
        header = f"{self.EMOJIS['thought']} Comandante Itamar, status da missão: {status}\n"
        body = f"--- REPORT ---\n{content}\n"
        footer = f"\n{self.EMOJIS['launch']} Sistemas em standby para o próximo comando."
        
        return header + body + footer

    def get_greeting(self, time_of_day):
        return f"Saudações, Comandante Itamar. Matriz de Engenharia {self.EMOJIS['thought']} pronta para agir."
