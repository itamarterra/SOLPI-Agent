import os
import requests
import hashlib
from bs4 import BeautifulSoup

class KnowledgeEngine:
    """
    MOTOR DE INGESTÃO E INDEXAÇÃO v80.3
    Transforma arquivos, códigos e sites em Memória Semântica de Longo Prazo.
    Gerencia o "Cérebro de Pesquisa" no drive E:.
    """
    def __init__(self, brain, knowledge_dir="E:/SOLPI-RESEARCH"):
        self.brain = brain
        self.knowledge_dir = knowledge_dir
        self.index = {} # Hash -> Metadata
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir, exist_ok=True)
        self._build_index()

    def _build_index(self):
        """Mapeia todos os arquivos técnicos no drive E:."""
        self.brain.kernel.log_event("KNOWLEDGE", "Indexando base de conhecimento técnica...")
        for root, _, files in os.walk(self.knowledge_dir):
            for f in files:
                if f.endswith(('.py', '.txt', '.md', '.json')):
                    path = os.path.join(root, f)
                    file_hash = hashlib.md5(path.encode()).hexdigest()
                    self.index[file_hash] = {
                        "name": f,
                        "path": path,
                        "size": os.path.getsize(path)
                    }

    def query_engine_intelligence(self, query):
        """Busca profunda no SOLPI-ENGINE e em Skills."""
        self.brain.kernel.log_event("RAG", f"Pesquisando contexto para: {query[:20]}")
        results = []
        
        # Busca prioritária em skills e core
        search_paths = ["E:/SOLPI-Agent/skills", "E:/SOLPI-Agent/core"]
        
        for sp in search_paths:
            if os.path.exists(sp):
                for root, _, files in os.walk(sp):
                    for f in files:
                        if f.endswith('.py'):
                            with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as content:
                                text = content.read()
                                if query.lower() in text.lower():
                                    results.append(f"🔍 Encontrado no código ({f}):\n{text[:300]}...")
        
        return results if results else ["Nenhuma referência direta encontrada no núcleo."]

    def get_local_intelligence(self, query):
        """Interface RAG padrão."""
        return self.query_engine_intelligence(query)
