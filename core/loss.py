import numpy as np

class SOLPICrossEntropyLoss:
    """
    PACOTE 0800: LOSS ENGINE v1.0
    Calcula o erro de predição categórica (Cross Entropy).
    """
    def __init__(self):
        self.eps = 1e-12

    def calculate(self, probs, target_idx):
        """
        probs: Vetor de probabilidades do Softmax
        target_idx: O ID real da próxima palavra
        """
        p = np.clip(probs, self.eps, 1. - self.eps)
        loss = -np.log(p[target_idx])
        return loss

    def gradient(self, probs, target_idx):
        """Gradiente da Softmax + CrossEntropy (Simplificado)."""
        grad = probs.copy()
        grad[target_idx] -= 1
        return grad
