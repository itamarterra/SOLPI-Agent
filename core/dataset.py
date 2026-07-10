import os

class SOLPIDataset:
    """
    PACOTE 1001: DATASET LOADER v1.0
    Indexa e carrega dados dos discos C: e E:.
    """
    def __init__(self, research_path="E:/SOLPI-RESEARCH", knowledge_path="C:/SOLPI-Agent/knowledge"):
        self.paths = [research_path, knowledge_path]
        self.file_index = []
        self.index_data()

    def index_data(self):
        """Varre os diretórios em busca de material de estudo (Etapa 1)."""
        print("📁 [DATASET]: Indexando bibliotecas de pesquisa no disco E: e C:...")
        for path in self.paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    # Ignora pastas de cache e git para manter a qualidade (Etapa 1004)
                    if '.git' in dirs: dirs.remove('.git')
                    if '__pycache__' in dirs: dirs.remove('__pycache__')
                    
                    for f in files:
                        if f.endswith(('.py', '.txt', '.cpp', '.h', '.php')):
                            self.file_index.append(os.path.join(root, f))
        print(f"✅ [DATASET]: {len(self.file_index)} fontes de conhecimento mapeadas.")

    def get_batch(self, size=5):
        """Retorna uma amostra de textos para o Transformer (Etapa 1101)."""
        import random
        samples = random.sample(self.file_index, min(size, len(self.file_index)))
        data = []
        for s in samples:
            try:
                with open(s, 'r', encoding='utf-8', errors='ignore') as f:
                    data.append(f.read(1000)) # Pega os primeiros 1000 caracteres
            except: continue
        return data
