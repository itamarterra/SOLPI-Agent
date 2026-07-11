import json
import os
import random

class SOLPISocialEngine:
    """
    PACOTE 5900: SOCIAL ENGINE v1.0
    Gerencia o Corpus de Diálogo (Perguntas e Respostas pré-definidas).
    Garante que o SOLPI-OS responda de forma humana e consistente.
    """
    def __init__(self, brain):
        self.brain = brain
        self.corpus_path = "E:/SOLPI-Agent/intelligence/corpus/dialogue_base.json"
        self.dialogue_data = {}
        self.load_corpus()

    def load_corpus(self):
        """Carrega a base de perguntas e respostas do JSON."""
        if os.path.exists(self.corpus_path):
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                self.dialogue_data = json.load(f)

    def get_response(self, user_input):
        """Tenta encontrar uma resposta mapeada para o input do usuário."""
        input_low = user_input.lower()
        
        for category, data in self.dialogue_data.items():
            # Verifica se alguma das perguntas gatilho está no input
            if any(trigger in input_low for trigger in data["perguntas"]):
                # Retorna uma resposta aleatória da categoria para não ser repetitivo
                return random.choice(data["respostas"])
        
        return None

    def add_to_corpus(self, category, trigger, response):
        """Permite expandir o corpus dinamicamente."""
        if category not in self.dialogue_data:
            self.dialogue_data[category] = {"perguntas": [], "respostas": []}
        
        if trigger not in self.dialogue_data[category]["perguntas"]:
            self.dialogue_data[category]["perguntas"].append(trigger)
        if response not in self.dialogue_data[category]["respostas"]:
            self.dialogue_data[category]["respostas"].append(response)
            
        with open(self.corpus_path, 'w', encoding='utf-8') as f:
            json.dump(self.dialogue_data, f, indent=4, ensure_ascii=False)
        return f"✅ Nova inteligência social adicionada à categoria {category}."
