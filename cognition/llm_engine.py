import os
import requests
import json

class LLMEngine:
    """
    Cérebro Híbrido SOLPI v6.2.
    Prioriza o OLLAMA (Grátis/Local) ou o Cérebro de Regras.
    """
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "local") # Mude para 'ollama' se instalar ele
        self.model = os.getenv("LLM_MODEL", "llama3")

    def chat(self, messages, tools=None):
        if self.provider == "ollama":
            return self._call_ollama(messages)
        
        # Se não tiver Ollama, usa o motor de regras gratuito do SOLPI
        return self._local_rule_brain(messages)

    def _call_ollama(self, messages):
        """Chama a IA rodando localmente no seu PC (Ollama)."""
        url = "http://localhost:11434/api/chat"
        payload = {"model": self.model, "messages": messages, "stream": False}
        try:
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            # Converte formato Ollama para o formato padrão SOLPI
            return {"choices": [{"message": {"content": data['message']['content']}}]}
        except:
            return {"error": "Ollama não detectado. Rode 'ollama serve' ou use o modo 'local'."}

    def _local_rule_brain(self, messages):
        """Motor de inteligência baseado em regras (100% grátis e leve)."""
        last_msg = messages[-1]['content'].lower()
        
        # Dicionário de Inteligência Gratuita
        knowledge = {
            "boa noite": "Boa noite, Comandante Itamar! Como está o sistema hoje?",
            "bom dia": "Bom dia! Pronto para os comandos.",
            "status": "O SOLPI OS está online. Modo Gratuito ativado.",
            "objetivo": "Entendido. Vou processar esse objetivo usando meus agentes locais.",
            "quem é você": "Eu sou o SOLPI OS, sua inteligência operacional local.",
            "ajuda": "Você pode usar comandos shell ($), tirar prints, ou pedir para eu abrir sites."
        }

        for key in knowledge:
            if key in last_msg:
                return {"choices": [{"message": {"content": knowledge[key]}}]}

        return {"choices": [{"message": {"content": f"Entendi sua mensagem: '{last_msg}'. O que deseja que eu execute?"}}]}
