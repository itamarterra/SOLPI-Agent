import numpy as np

class SOLPIFeedForward:
    """
    PACOTE 6400: FEED FORWARD ENGINE v50.0
    Implementa MLP com ativação GELU ou SwiGLU.
    """
    def __init__(self, dim, hidden_dim):
        self.W1 = np.random.randn(dim, hidden_dim) * 0.02
        self.W2 = np.random.randn(hidden_dim, dim) * 0.02

    def forward(self, x):
        # GELU Activation
        hidden = np.dot(x, self.W1)
        hidden = hidden * 0.5 * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (hidden + 0.044715 * np.power(hidden, 3))))
        return np.dot(hidden, self.W2)
