import numpy as np

class SOLPIEmbeddingEngine:
    """
    PACOTE 6200: EMBEDDING ENGINE v50.6 (Depth: RoPE)
    Implementa Rotary Positional Embeddings para precisão semântica superior.
    """
    def __init__(self, vocab_size, embed_dim, max_seq_len=2048):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.weights = np.random.randn(vocab_size, embed_dim) * 0.01
        
        # Pré-computa frequências para RoPE
        self.inv_freq = 1.0 / (10000 ** (np.arange(0, embed_dim, 2).astype(np.float32) / embed_dim))

    def _apply_rope(self, x, seq_len):
        """Aplica a rotação nos embeddings baseada na posição."""
        t = np.arange(seq_len)
        freqs = np.outer(t, self.inv_freq)
        emb = np.concatenate((freqs, freqs), axis=-1)
        
        # Rotação complexa simulada
        cos_emb = np.cos(emb)
        sin_emb = np.sin(emb)
        
        # x_rotated = (x * cos) + (rotate_half(x) * sin)
        x2 = np.concatenate((-x[..., self.embed_dim//2:], x[..., :self.embed_dim//2]), axis=-1)
        return (x * cos_emb) + (x2 * sin_emb)

    def forward(self, tokens):
        """Busca vetores e aplica RoPE."""
        x = self.weights[tokens]
        seq_len = x.shape[0] if len(x.shape) == 2 else x.shape[1]
        
        # Aplica RoPE se for 3D (batch, seq, dim) ou 2D (seq, dim)
        if len(x.shape) == 3:
            for b in range(x.shape[0]):
                x[b] = self._apply_rope(x[b], seq_len)
        else:
            x = self._apply_rope(x, seq_len)

        return x
