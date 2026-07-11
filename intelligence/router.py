import numpy as np

class SOLPISemanticRouter:
    """
    PACOTE 8200: SEMANTIC ROUTER v1.0
    Substitui o Supervisor de if/else por uma decisão baseada em similaridade vetorial.
    Decide qual Expert deve tratar a entrada baseado no 'espaço semântico'.
    """
    def __init__(self, brain):
        self.brain = brain
        self.expert_embeddings = {}
        self._initialize_expert_vectors()

    def _initialize_expert_vectors(self):
        """Inicializa vetores 'âncora' para cada especialidade."""
        # Em um sistema real, estes seriam embeddings de descrições ricas.
        # Aqui, usamos o próprio NativeCore para gerar vetores baseados em keywords semânticas.
        anchors = {
            "INFRA_EXPERT": "status rede zabbix docker servidor infraestrutura porta conexão",
            "SQL_EXPERT": "listar chamados banco dados sql maria db ativos hardware usuários",
            "DEV_EXPERT": "código python php script erro correção programa algoritmo função",
            "VISION_EXPERT": "tela screenshot print veja olhe captura visão imagem"
        }
        
        for expert, text in anchors.items():
            self.expert_embeddings[expert] = self.get_sentence_embedding(text)

    def get_sentence_embedding(self, text):
        """Gera um vetor único para uma frase (Mean Pooling)."""
        tokens = self.brain.native_core.tokenizer.encode(text)
        if not tokens: return np.zeros(self.brain.native_core.config.EMBED_DIM)
        
        # Pega os embeddings dos tokens do NeuralRuntime v50
        token_vecs = self.brain.native_core.embedding_engine.weights[tokens]
        return np.mean(token_vecs, axis=0)

    def route(self, user_input):
        """Calcula similaridade de cosseno para decidir o destino."""
        input_vec = self.get_sentence_embedding(user_input)
        
        best_expert = "GENERALIST"
        max_sim = -1.0
        
        for expert, expert_vec in self.expert_embeddings.items():
            # Similaridade de Cosseno
            sim = np.dot(input_vec, expert_vec) / (np.linalg.norm(input_vec) * np.linalg.norm(expert_vec) + 1e-9)
            
            if sim > max_sim:
                max_sim = sim
                best_expert = expert
                
        # Limiar de confiança para roteamento semântico
        if max_sim < 0.2:
            return "GENERALIST", "Confiança semântica baixa. Usando orquestrador genérico."
            
        return best_expert, f"Roteado semanticamente para {best_expert} (Confiança: {max_sim:.2f})"
