import json
import os
import random

class SOLPISocialEngine:
    """
    PACOTE 5900: SOCIAL DIALOGUE ENGINE v70.2
    Gerencia a 'Área de Diálogo' baseada em bibliotecas JSON.
    Permite customizar todas as perguntas e respostas do sistema.
    """
    def __init__(self, brain):
        self.brain = brain
        self.dialogue_dir = "E:/SOLPI-Agent/intelligence/knowledge/dialogue"
        self.knowledge_base = {}
        self.load_dialogues()

    def load_dialogues(self):
        """Carrega os arquivos de diálogo JSON."""
        if not os.path.exists(self.dialogue_dir):
            os.makedirs(self.dialogue_dir, exist_ok=True)
            return
            
        for file in os.listdir(self.dialogue_dir):
            if file.endswith(".json"):
                path = os.path.join(self.dialogue_dir, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.knowledge_base.update(data)
                except Exception as e:
                    self.brain.kernel.log_event("ERROR", f"Falha ao carregar diálogo {file}: {e}")

    def get_response(self, user_input):
        """Busca se a pergunta do usuário está mapeada na biblioteca."""
        input_low = user_input.lower().strip()
        
        for category, content in self.knowledge_base.items():
            # Verifica se alguma pergunta mapeada está no input do usuário
            for p in content.get("perguntas", []):
                if p.lower() in input_low:
                    return random.choice(content["respostas"])
        
        return None
