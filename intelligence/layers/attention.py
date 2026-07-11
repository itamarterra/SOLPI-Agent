import numpy as np

class SOLPIAttentionEngine:
    """
    PACOTE 6100: ATTENTION ENGINE v50.0
    Implementa variantes de Attention (GQA, Flash-sim, MQA).
    Baseado em arquiteturas de alto throughput (Llama-3).
    """
    def __init__(self, embed_dim, n_heads=8, n_kv_heads=2):
        self.embed_dim = embed_dim
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.head_dim = embed_dim // n_heads
        self.kv_group_size = n_heads // n_kv_heads
        
        # Pesos Q, K, V, O
        self.W_q = np.random.randn(embed_dim, n_heads * self.head_dim) * 0.02
        self.W_k = np.random.randn(embed_dim, n_kv_heads * self.head_dim) * 0.02
        self.W_v = np.random.randn(embed_dim, n_kv_heads * self.head_dim) * 0.02
        self.W_o = np.random.randn(n_heads * self.head_dim, embed_dim) * 0.02

    def forward(self, x, mask=None):
        """Forward pass com suporte a Grouped-Query Attention."""
        batch_size, seq_len, _ = x.shape if len(x.shape) == 3 else (1, x.shape[0], x.shape[1])
        
        # Projeções
        q = np.dot(x, self.W_q).reshape(batch_size, seq_len, self.n_heads, self.head_dim).transpose(0, 2, 1, 3)
        k = np.dot(x, self.W_k).reshape(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(0, 2, 1, 3)
        v = np.dot(x, self.W_v).reshape(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(0, 2, 1, 3)

        # Repetição de K/V para GQA (Grouped Query)
        if self.kv_group_size > 1:
            k = np.repeat(k, self.kv_group_size, axis=1)
            v = np.repeat(v, self.kv_group_size, axis=1)

        # Scaled Dot-Product Attention
        scores = np.matmul(q, k.transpose(0, 1, 3, 2)) / np.sqrt(self.head_dim)
        
        if mask is not None:
            scores += mask

        probs = self.softmax(scores)
        
        # Output Projection
        out = np.matmul(probs, v).transpose(0, 2, 1, 3).reshape(batch_size, seq_len, -1)
        return np.dot(out, self.W_o)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)
