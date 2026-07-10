import numpy as np

class SOLPIRMSNorm:
    # ... (já implementado) ...
    pass

class SOLPILayerNorm:
    """
    PACOTE 0500: LAYER NORM v1.0
    Normalização clássica (Média e Variância).
    Estabiliza o treinamento (Etapa 10).
    """
    def __init__(self, dim, eps=1e-5):
        self.eps = eps
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)

    def forward(self, x):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        x_norm = (x - mean) / np.sqrt(var + self.eps)
        return self.gamma * x_norm + self.beta
