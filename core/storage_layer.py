import json
import os

class SOLPIStorageLayer:
    """
    PACOTE 8900: STORAGE API v1.0
    Unifica a persistência de dados (JSON, SQLite, Vetorial).
    Nenhum módulo deve salvar arquivos diretamente.
    """
    def __init__(self, brain):
        self.brain = brain
        self.base_path = "E:/SOLPI-DATA"
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)

    def save_json(self, namespace, filename, data):
        target_dir = os.path.join(self.base_path, namespace)
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, f"{filename}.json")
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return path

    def load_json(self, namespace, filename):
        path = os.path.join(self.base_path, namespace, f"{filename}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
