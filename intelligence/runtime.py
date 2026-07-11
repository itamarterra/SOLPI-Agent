import numpy as np
from intelligence.layers.tokenizer import SOLPITokenizer
from intelligence.layers.embeddings import SOLPIEmbeddingEngine
from intelligence.layers.attention import SOLPIAttentionEngine
from intelligence.layers.norm import SOLPIRMSNorm
from intelligence.layers.feed_forward import SOLPIFeedForward
from core.config import SOLPIConfig

class SOLPITransformerBlock:
    """Bloco Transformer Completo (Attention + FeedForward + Residual + Norm)"""
    def __init__(self, config):
        self.attn = SOLPIAttentionEngine(config.EMBED_DIM, config.NUM_HEADS, config.NUM_KV_HEADS)
        self.ffn = SOLPIFeedForward(config.EMBED_DIM, config.EMBED_DIM * 4)
        self.norm1 = SOLPIRMSNorm(config.EMBED_DIM)
        self.norm2 = SOLPIRMSNorm(config.EMBED_DIM)

    def forward(self, x):
        # Attention + Residual
        x = x + self.attn.forward(self.norm1.forward(x))
        # FeedForward + Residual
        x = x + self.ffn.forward(self.norm2.forward(x))
        return x

class SOLPINeuralRuntime:
    """
    PACOTE 6000: NEURAL RUNTIME v50.0
    Orquestrador de execução de modelos. Abstrai a complexidade do Transformer.
    """
    def __init__(self, config=None):
        self.config = config or SOLPIConfig()
        self.tokenizer = SOLPITokenizer()
        self.embedding_engine = SOLPIEmbeddingEngine(self.config.VOCAB_SIZE, self.config.EMBED_DIM)
        
        # Pilha de Blocos Transformer (Depth!)
        self.blocks = [SOLPITransformerBlock(self.config) for _ in range(self.config.NUM_LAYERS)]
        self.final_norm = SOLPIRMSNorm(self.config.EMBED_DIM)
        
        # Projeção de Saída
        self.output_projection = np.random.randn(self.config.EMBED_DIM, self.config.VOCAB_SIZE) * 0.02

    def forward(self, tokens):
        """Passagem completa pelo modelo."""
        # Embeddings + Positional Encoding
        x = self.embedding_engine.forward(tokens)
        
        # Dimension matching para batch se necessário
        if len(x.shape) == 2: x = x[np.newaxis, :, :]

        # Passagem pelos blocos
        for block in self.blocks:
            x = block.forward(x)
            
        x = self.final_norm.forward(x)
        return x[0] if x.shape[0] == 1 else x

    def get_logits(self, tokens):
        hidden = self.forward(tokens)
        last_hidden = hidden[-1] if len(hidden.shape) == 2 else hidden[:, -1, :]
        return np.dot(last_hidden, self.output_projection)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)

    def get_trainable_params(self):
        """Coleta parâmetros de toda a profundidade da rede."""
        params = [self.embedding_engine.weights, self.output_projection]
        for block in self.blocks:
            params += [block.attn.W_q, block.attn.W_k, block.attn.W_v, block.attn.W_o]
            params += [block.ffn.W1, block.ffn.W2]
        return params

    def think_native(self, text):
        tokens = self.tokenizer.encode(text)
        if not tokens: return "Entrada vazia."
        _ = self.forward(tokens)
        return f"🧠 [NEURAL-RUNTIME v50]: Processado via {len(self.blocks)} camadas Transformer de alta performance."
