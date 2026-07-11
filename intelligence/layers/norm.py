import numpy as np

class SOLPIRMSNorm:
    """
    PACOTE 6300: NORM ENGINE v50.0
    Root Mean Square Layer Normalization (Llama style).
    Mais estável para treinamento de larga escala.
    """
    def __init__(self, dim, eps=1e-6):
        self.eps = eps
        self.weight = np.ones(dim)

    def forward(self, x):
        norm = np.sqrt(np.mean(x**2, axis=-1, keepdims=True) + self.eps)
        return self.weight * (x / norm)
