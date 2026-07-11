import numpy as np

class SOLPIEmbeddingEngine:
    """
    PACOTE 6200: EMBEDDING ENGINE v50.0
    Gerencia Embeddings e integra Positional Encoding (RoPE/Absolute).
    """
    def __init__(self, vocab_size, embed_dim, max_seq_len=512):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.weights = np.random.randn(vocab_size, embed_dim) * 0.01
        
        # Absolute Positional Encoding (Fase 1)
        self.pos_encoding = self._generate_pos_encoding(max_seq_len, embed_dim)

    def _generate_pos_encoding(self, length, dim):
        encoding = np.zeros((length, dim))
        for pos in range(length):
            for i in range(0, dim, 2):
                encoding[pos, i] = np.sin(pos / (10000 ** (i / dim)))
                if i + 1 < dim:
                    encoding[pos, i + 1] = np.cos(pos / (10000 ** (i / dim)))
        return encoding

    def forward(self, tokens, add_pos=True):
        """Busca vetores e opcionalmente adiciona informação de posição."""
        x = self.weights[tokens]
        if add_pos:
            seq_len = x.shape[0] if len(x.shape) == 2 else x.shape[1]
            if seq_len <= self.pos_encoding.shape[0]:
                if len(x.shape) == 3:
                    x += self.pos_encoding[:seq_len, :][np.newaxis, :, :]
                else:
                    x += self.pos_encoding[:seq_len, :]
        return x
