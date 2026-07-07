import os
import requests
import json

class LLMEngine:
    """
    O Cérebro do SOLPI OS v6.0.
    Abstração universal para múltiplos provedores de IA.
    """
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai") # openai, ollama, gemini
        self.api_key = os.getenv("LLM_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-4o")

    def chat(self, messages, tools=None):
        """Ponto de entrada único para conversação e chamada de ferramentas."""
        if self.provider == "openai":
            return self._call_openai(messages, tools)
        elif self.provider == "ollama":
            return self._call_ollama(messages, tools)
        return {"error": "Provedor não suportado."}

    def _call_openai(self, messages, tools):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "temperature": 0.3
        }
        try:
            res = requests.post(url, headers=headers, json=payload)
            return res.json()
        except Exception as e:
            return {"error": str(e)}

    def _call_ollama(self, messages, tools):
        # Implementação local do Ollama para modo offline
        url = "http://localhost:11434/api/chat"
        payload = {"model": "llama3", "messages": messages, "stream": False}
        res = requests.post(url, json=payload)
        return res.json()
