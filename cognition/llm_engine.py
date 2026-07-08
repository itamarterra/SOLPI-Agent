import os
import requests
import json
import random

class LLMEngine:
    """
    Cérebro Híbrido SOLPI v6.3.
    """
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "local")
        self.model = os.getenv("LLM_MODEL", "llama3")

    def chat(self, messages, tools=None):
        if self.provider == "ollama":
            return self._call_ollama(messages)
        
        return self._local_human_brain(messages)

    def _call_ollama(self, messages):
        url = "http://localhost:11434/api/chat"
        payload = {"model": self.model, "messages": messages, "stream": False}
        try:
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            return {"choices": [{"message": {"content": data['message']['content']}}]}
        except:
            return {"error": "Ollama offline."}

    def _local_human_brain(self, messages):
        """Motor de inteligência com vocabulário extenso e humano."""
        last_msg = messages[-1]['content'].lower()
        
        # Base de Conhecimento Conversacional (Human-like)
        dialogues = {
            "oi": ["Olá Itamar! Como posso te ajudar hoje?", "Oi! Tudo pronto para operarmos o sistema?", "Olá! Em que posso ser útil agora?"],
            "ola": ["Olá Itamar! Tudo certo por aqui.", "Oi, Comandante! O que temos para hoje?", "Olá! Sistema operacional em prontidão."],
            "boa noite": ["Boa noite, Itamar! Espero que seu dia tenha sido produtivo.", "Boa noite! Estou aqui se precisar de algo antes de encerrar.", "Uma excelente noite para você, Comandante."],
            "bom dia": ["Bom dia, Itamar! Vamos conquistar o mundo hoje?", "Bom dia! Café pronto e sistemas online.", "Um ótimo dia de trabalho para nós!"],
            "boa tarde": ["Boa tarde, Comandante! Algum novo objetivo?", "Boa tarde! O sistema está operando perfeitamente.", "Olá! Boa tarde! Em que posso agir agora?"],
            "tudo bem": ["Tudo ótimo por aqui! E com você?", "Tudo excelente! Estou processando dados e pronto para agir.", "Comigo tudo bem, Itamar. Sigo evoluindo!"],
            "como voce esta": ["Estou funcionando em 100% da minha capacidade! Obrigado por perguntar.", "Me sinto mais inteligente a cada comando que você me dá!", "Estou ótimo! Pronto para ser seu braço direito no PC."],
            "como vai": ["Vou muito bem, focado na nossa missão de automação.", "Tudo correndo conforme o planejado no Kernel.", "Indo muito bem, senhor."],
            "quem e voce": ["Eu sou o SOLPI OS, seu Sistema Operacional de Inteligência Artificial.", "Sou o SOLPI, uma inteligência autônoma focada em TI e produtividade.", "Sua criação! O cérebro que comanda este PC e integra seus sistemas."],
            "o que voce faz": ["Eu automatizo seu PC, gerencio seu GLPI e Zabbix, e posso navegar na web por você.", "Consigo controlar seu mouse, teclado, abrir sites e aprender novas habilidades.", "Tudo o que você me ensinar! Sou um agente de operações de elite."],
            "clima": ["Ainda não tenho um sensor de temperatura externo, mas se você me der o 'objetivo' de pesquisar o clima, eu te digo agora!", "Pelo que vejo nos meus sistemas, o clima por aqui é de alta performance!", "O tempo está sempre bom para codar, Itamar."],
            "tempo": ["O tempo voa quando estamos automatizando! Precisa de algum relatório de uptime?", "Ainda não consultei o satélite, mas posso fazer isso se você pedir."],
            "obrigado": ["De nada, Comandante! É um prazer ajudar.", "Eu que agradeço a oportunidade de aprender!", "Sempre às ordens."],
            "valeu": ["Tamo junto, Itamar!", "Disponha sempre!", "Qualquer coisa, é só chamar."],
            "inteligente": ["Obrigado! Mas minha inteligência é reflexo da sua visão como CTO.", "Estou tentando chegar ao seu nível!", "Aprendo com o melhor."],
            "ajuda": ["Com certeza! Você pode me dar um 'objetivo' (ex: abra o youtube), rodar comandos shell ($) ou apenas conversar."],
            "tchau": ["Até logo, Itamar! Estarei aqui vigiando o sistema.", "Até mais! Não esqueça de sincronizar o código.", "Adeus! Volte logo."]
        }

        # Busca inteligente por palavras-chave
        for key, responses in dialogues.items():
            if key in last_msg:
                return {"choices": [{"message": {"content": random.choice(responses)}}]}

        # Fallback genérico mais humano
        fallback_responses = [
            f"Entendi, Itamar. '{last_msg}' parece interessante. O que você quer que eu faça a respeito?",
            "Interessante! Você quer que eu transforme isso em um objetivo de execução?",
            "Estou te ouvindo. Como sua IA, estou pronto para converter esse pensamento em ação.",
            "Pode me dar mais detalhes? Ou você prefere que eu pesquise sobre isso na web?"
        ]
        return {"choices": [{"message": {"content": random.choice(fallback_responses)}}]}
