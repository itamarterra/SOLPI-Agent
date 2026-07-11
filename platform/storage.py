import json
import os

class SOLPIStorage:
    """
    PACOTE 8900: STORAGE LAYER v50.3
    API centralizada para persistência de dados no Domínio de Plataforma.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.base_dir = "E:/SOLPI-DATA"
        if not os.path.exists(self.base_dir): os.makedirs(self.base_dir, exist_ok=True)

    def write_json(self, domain, name, data):
        path = os.path.join(self.base_dir, domain)
        if not os.path.exists(path): os.makedirs(path, exist_ok=True)
        file = os.path.join(path, f"{name}.json")
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return file

    def read_json(self, domain, name):
        file = os.path.join(self.base_dir, domain, f"{name}.json")
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
