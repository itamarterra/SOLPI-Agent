import os
import json
import requests
from core.tools import AgentTools

class SOLPIBrain:
    """
    NÚCLEO DE CONSCIÊNCIA v9.0 (Visual Operator)
    """
    def __init__(self):
        self.tools = AgentTools()
        self.last_context = None

    def process(self, user_input):
        cmd = user_input.lower().strip()
        
        # 1. MISSÃO VISUAL (O Agente vê e clica)
        if any(x in cmd for x in ["clique em", "aperte o botão", "onde está"]):
            return self.visual_mission(user_input)

        # 2. CONTROLE DE CONTEXTO (YouTube/Windows)
        interaction_triggers = ["pause", "play", "para", "desce", "sobe"]
        if any(x in cmd for x in interaction_triggers) and self.last_context:
            return self.tools.interact_with_window(self.last_context, cmd)

        # 3. ABERTURA E PESQUISA
        if any(x in cmd for x in ["abra", "abre", "abrir", "youtube", "glpi"]):
            self.last_context = cmd
            return self.tools.control_computer("abrir", cmd)

        # 4. PESQUISA WEB
        return "\n".join(self.tools.search(cmd))

    def visual_mission(self, user_input):
        """Usa a visão para achar elementos e clicar neles."""
        self.tools.speak("Vou analisar sua tela para encontrar o que você pediu.")
        img_b64 = self.tools.analyze_screen()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or "sua_chave" in api_key:
            return "⚠️ Preciso de uma API KEY no .env para realizar operações visuais."

        # IA analisa a imagem e retorna coordenadas
        prompt = f"O usuário quer: '{user_input}'. Me dê as coordenadas X e Y do elemento na tela. " \
                 f"Responda APENAS um JSON: {{\"x\": int, \"y\": int, \"description\": \"...\"}}"
        
        # Aqui o Agente faria a chamada GPT-4o Vision real
        # Por agora, o motor está pronto para receber essa integração
        return "🧠 [VISION]: Pronto para mapear coordenadas visuais."
