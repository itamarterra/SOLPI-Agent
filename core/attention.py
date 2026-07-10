import numpy as np

class SOLPIGQA:
    """
    PACOTE 08: GROUPED-QUERY ATTENTION (GQA) v40.0
    Otimização Enterprise para redução de KV Cache e maior throughput.
    Baseado na arquitetura Llama-3.
    """
    def __init__(self, embed_dim, n_heads=8, n_kv_heads=2):
        self.embed_dim = embed_dim
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.head_dim = embed_dim // n_heads
        self.kv_group_size = n_heads // n_kv_heads
        
        # Pesos Q, K, V
        self.W_q = np.random.randn(embed_dim, n_heads * self.head_dim) * 0.02
        self.W_k = np.random.randn(embed_dim, n_kv_heads * self.head_dim) * 0.02
        self.W_v = np.random.randn(embed_dim, n_kv_heads * self.head_dim) * 0.02
        self.W_o = np.random.randn(n_heads * self.head_dim, embed_dim) * 0.02

    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape if len(x.shape) == 3 else (1, x.shape[0], x.shape[1])
        
        # Projeções
        queries = np.dot(x, self.W_q) # (B, L, H_q * D)
        keys = np.dot(x, self.W_k)    # (B, L, H_kv * D)
        values = np.dot(x, self.W_v)  # (B, L, H_kv * D)

        # Reshape para Heads
        queries = queries.reshape(batch_size, seq_len, self.n_heads, self.head_dim).transpose(0, 2, 1, 3)
        keys = keys.reshape(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(0, 2, 1, 3)
        values = values.reshape(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(0, 2, 1, 3)

        # Expandir K e V para o número de Query Heads (Repetição para GQA)
        keys = np.repeat(keys, self.kv_group_size, axis=1)
        values = np.repeat(values, self.kv_group_size, axis=1)

        # Scaled Dot-Product Attention
        scores = np.matmul(queries, keys.transpose(0, 1, 3, 2)) / np.sqrt(self.head_dim)
        
        if mask is not None:
            scores += mask

        probs = self.softmax(scores)
        
        # Saída
        out = np.matmul(probs, values) # (B, H, L, D)
        out = out.transpose(0, 2, 1, 3).reshape(batch_size, seq_len, -1)
        
        return np.dot(out, self.W_o)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)

# Alias para compatibilidade se necessário
SOLPISelfAttention = SOLPIGQA
