import numpy as np

class CPUBackend:
    """
    PACOTE 1600: CPU BACKEND v1.0
    Implementação otimizada via NumPy para execução em processadores.
    """
    @staticmethod
    def dot(a, b):
        return np.dot(a, b)

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def rms_norm(x, weight, eps=1e-6):
        norm = np.sqrt(np.mean(x**2, axis=-1, keepdims=True) + eps)
        return weight * (x / norm)
