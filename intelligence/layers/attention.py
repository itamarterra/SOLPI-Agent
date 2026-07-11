import numpy as np

class SOLPIAttentionEngine:
    """
    PACOTE 6100: ATTENTION ENGINE v50.6 (Depth: Optimized GQA)
    Implementa Grouped-Query Attention com otimização de cache KV.
    """
    def __init__(self, embed_dim, n_heads=8, n_kv_heads=2):
        self.embed_dim = embed_dim
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.head_dim = embed_dim // n_heads
        self.kv_group_size = n_heads // n_kv_heads
        
        # Pesos com inicialização Xavier/Kaiming para estabilidade
        scale = np.sqrt(2.0 / (embed_dim + embed_dim))
        self.W_q = np.random.randn(embed_dim, n_heads * self.head_dim) * scale
        self.W_k = np.random.randn(embed_dim, n_kv_heads * self.head_dim) * scale
        self.W_v = np.random.randn(embed_dim, n_kv_heads * self.head_dim) * scale
        self.W_o = np.random.randn(n_heads * self.head_dim, embed_dim) * scale

    def forward(self, x, mask=None):
        """Forward pass otimizado com redução de operações redundantes."""
        batch_size, seq_len, _ = x.shape if len(x.shape) == 3 else (1, x.shape[0], x.shape[1])
        
        # Projeções Lineares
        q = np.dot(x, self.W_q).reshape(batch_size, seq_len, self.n_heads, self.head_dim).transpose(0, 2, 1, 3)
        k = np.dot(x, self.W_k).reshape(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(0, 2, 1, 3)
        v = np.dot(x, self.W_v).reshape(batch_size, seq_len, self.n_kv_heads, self.head_dim).transpose(0, 2, 1, 3)

        # GQA: Repetição eficiente de K/V
        if self.kv_group_size > 1:
            k = np.repeat(k, self.kv_group_size, axis=1)
            v = np.repeat(v, self.kv_group_size, axis=1)

        # Atencão de Produto Escalar Escalonado
        # scores = (Q @ K^T) / sqrt(d_k)
        scores = np.matmul(q, k.transpose(0, 1, 3, 2)) / np.sqrt(self.head_dim)
        
        if mask is not None:
            scores += mask

        # Softmax com estabilidade numérica
        probs = self.softmax(scores)
        
        # Saída: Context Vector
        context = np.matmul(probs, v).transpose(0, 2, 1, 3).reshape(batch_size, seq_len, -1)
        return np.dot(context, self.W_o)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)
