import json
import os
import time
import numpy as np

class SOLPIFeatureStore:
    """
    PACOTE 9300: FEATURE STORE v1.0
    Sistema de Cache de Embeddings e Predições para Otimização de Latência.
    Reduz o custo computacional ao evitar re-processamento de inputs similares.
    """
    def __init__(self, brain):
        self.brain = brain
        self.store_path = "E:/SOLPI-DATA/features"
        self.cache = {}
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path, exist_ok=True)
        self._load_warm_cache()

    def _load_warm_cache(self):
        """Carrega as features mais usadas na inicialização."""
        try:
            path = os.path.join(self.store_path, "registry.json")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self.cache = json.load(f)
        except: pass

    def get_feature(self, query):
        """Busca se já existe um embedding/resposta para esta query."""
        query_hash = str(hash(query))
        if query_hash in self.cache:
            self.brain.kernel.log_event("FEATURE_STORE", "Cache Hit: Recuperando feature otimizada.")
            return self.cache[query_hash]
        return None

    def save_feature(self, query, feature_data):
        """Salva uma predição/vetor no store."""
        query_hash = str(hash(query))
        feature_entry = {
            "timestamp": time.time(),
            "data": feature_data,
            "access_count": 1
        }
        self.cache[query_hash] = feature_entry
        
        # Persistência assíncrona (simulada via Scheduler futuramente)
        with open(os.path.join(self.store_path, "registry.json"), 'w') as f:
            json.dump(self.cache, f)

    def optimize_latency(self, query, fallback_fn, *args):
        """Tenta retornar do cache, se não rodar a função pesada."""
        cached = self.get_feature(query)
        if cached:
            return cached["data"]
        
        # Se não tem no cache, executa e salva
        result = fallback_fn(*args)
        self.save_feature(query, result)
        return result
