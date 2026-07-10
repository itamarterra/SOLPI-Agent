import numpy as np

class SOLPISelfAttention:
    """
    PACOTE 08: ATTENTION v2.0
    Agora com PACOTE 0608: KV Cache para inferência de alta performance.
    """
    def __init__(self, embed_dim):
        self.embed_dim = embed_dim
        self.W_q = np.random.randn(embed_dim, embed_dim) * np.sqrt(1/embed_dim)
        self.W_k = np.random.randn(embed_dim, embed_dim) * np.sqrt(1/embed_dim)
        self.W_v = np.random.randn(embed_dim, embed_dim) * np.sqrt(1/embed_dim)
        
        # KV Cache (Fase 18)
        self.k_cache = None
        self.v_cache = None

    def forward(self, x, use_cache=True):
        Q = np.dot(x, self.W_q)
        K = np.dot(x, self.W_k)
        V = np.dot(x, self.W_v)

        if use_cache:
            if self.k_cache is None:
                self.k_cache, self.v_cache = K, V
            else:
                self.k_cache = np.concatenate([self.k_cache, K], axis=0)
                self.v_cache = np.concatenate([self.v_cache, V], axis=0)
            K, V = self.k_cache, self.v_cache

        scores = np.dot(Q, K.T) / np.sqrt(self.embed_dim)
        weights = self.softmax(scores)
        return np.dot(weights, V)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)
