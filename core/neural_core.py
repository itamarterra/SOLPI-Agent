import numpy as np
from core.tokenizer import SOLPITokenizer
from core.attention import SOLPIGQA
from core.layer_norm import SOLPIRMSNorm
from core.feed_forward import SOLPIFeedForward
from core.config import SOLPIConfig

class SOLPIExpertLayer:
    """PACOTE 0103: Mixture of Experts (MoE) Specialist"""
    def __init__(self, embed_dim):
        self.experts = [SOLPIFeedForward(embed_dim, embed_dim * 4) for _ in range(4)]
        self.router = np.random.randn(embed_dim, 4) * 0.02
        self.routing_stats = {0: 0, 1: 0, 2: 0, 3: 0}

    def forward(self, x):
        # Roteamento: decide qual especialista melhor atende este token
        router_logits = np.dot(x, self.router)
        expert_idx = np.argmax(router_logits, axis=-1)
        
        # Estatísticas para o Reflection Engine
        for idx in expert_idx.flatten():
            self.routing_stats[int(idx)] += 1
            
        out = np.zeros_like(x)
        for i in range(4):
            mask = (expert_idx == i)
            if np.any(mask):
                out[mask] = self.experts[i].forward(x[mask])
        return out

class SOLPINeuralCore:
    def __init__(self):
        self.config = SOLPIConfig()
        self.tokenizer = SOLPITokenizer()
        self.norm = SOLPIRMSNorm(self.config.EMBED_DIM)
        # Implementação GQA (v40.0)
        self.attention = SOLPIGQA(self.config.EMBED_DIM, n_heads=self.config.NUM_HEADS, n_kv_heads=self.config.NUM_KV_HEADS)
        self.moe = SOLPIExpertLayer(self.config.EMBED_DIM)
        
        self.embeddings = np.random.randn(self.config.VOCAB_SIZE, self.config.EMBED_DIM) * 0.01
        self.output_projection = np.random.randn(self.config.EMBED_DIM, self.config.VOCAB_SIZE) * 0.02

    def forward(self, tokens):
        """Fluxo completo do Transformer"""
        x = self.embeddings[tokens] # (L, D)
        
        # Adiciona dimensão de Batch se necessário
        if len(x.shape) == 2:
            x_input = x[np.newaxis, :, :]
        else:
            x_input = x
            
        x_norm = self.norm.forward(x_input)
        
        # GQA Attention
        attn_out = self.attention.forward(x_norm)
        x_res = x_input + attn_out
        
        # MoE Layer
        moe_out = self.moe.forward(x_res)
        x_final = x_res + moe_out
        
        return x_final[0] if len(x.shape) == 2 else x_final

    def get_logits(self, tokens):
        """Retorna logits para o Trainer (Etapa 11)"""
        hidden = self.forward(tokens)
        last_hidden = hidden[-1] if len(hidden.shape) == 2 else hidden[:, -1, :]
        logits = np.dot(last_hidden, self.output_projection)
        return logits

    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)

    def get_trainable_params(self):
        """Coleta todos os tensores de peso para o otimizador"""
        params = [self.embeddings, self.output_projection]
        # Adiciona pesos da atenção GQA
        params += [self.attention.W_q, self.attention.W_k, self.attention.W_v, self.attention.W_o]
        # Adiciona pesos dos especialistas MoE
        params += [self.moe.router]
        for exp in self.moe.experts:
            params += [exp.W1, exp.W2]
        return params

    def think_native(self, text):
        tokens = self.tokenizer.encode(text)
        if not tokens: return "Vazio"
        
        # Ativa o processamento
        _ = self.forward(tokens)
        
        return f"🧠 [GQA-MOE v40.0]: Processado com Grouped-Query Attention e 4 Especialistas Neurais."
