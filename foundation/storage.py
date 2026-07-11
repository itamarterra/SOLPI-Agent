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
        # 🟢 Validação de Path Traversal (v70.0)
        safe_path = self.kernel.security.validate_path(self.base_dir, os.path.join(domain, f"{name}.json"))
        
        path = os.path.dirname(safe_path)
        if not os.path.exists(path): os.makedirs(path, exist_ok=True)
        
        with open(safe_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return safe_path

    def read_json(self, domain, name):
        safe_path = self.kernel.security.validate_path(self.base_dir, os.path.join(domain, f"{name}.json"))
        if os.path.exists(safe_path):
            with open(safe_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
