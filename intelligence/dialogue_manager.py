import json
import os
import random

class SOLPIDialogueManager:
    """
    PACOTE 5900: DIALOGUE MANAGER v1.0
    Central de respostas e perguntas predefinidas (Base de Diálogo).
    Gerencia a 'Bibliotecas de Respostas' do SOLPI-OS.
    """
    def __init__(self, brain):
        self.brain = brain
        self.dialogue_dir = "E:/SOLPI-Agent/intelligence/knowledge/dialogue"
        self.knowledge_base = {}
        self.load_dialogues()

    def load_dialogues(self):
        """Carrega todos os arquivos JSON da pasta de diálogos."""
        if not os.path.exists(self.dialogue_dir):
            return
            
        for file in os.listdir(self.dialogue_dir):
            if file.endswith(".json"):
                path = os.path.join(self.dialogue_dir, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.knowledge_base.update(data)
                except Exception as e:
                    self.brain.kernel.log_event("ERROR", f"Erro ao carregar diálogo {file}: {e}")

    def find_response(self, user_input):
        """Busca uma resposta adequada na base de conhecimento."""
        input_low = user_input.lower()
        
        for category, content in self.knowledge_base.items():
            for p in content["perguntas"]:
                if p in input_low:
                    # Retorna uma resposta aleatória da categoria para parecer mais humano
                    return random.choice(content["respostas"])
        
        return None
