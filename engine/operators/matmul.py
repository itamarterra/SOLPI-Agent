import numpy as np

class MatMul:
    """
    PACOTE 4001: MATMUL OPERATOR
    Implementação desacoplada da operação de Multiplicação de Matrizes.
    """
    @staticmethod
    def forward(ctx, a, b):
        """
        a, b: SOLPITensor objects
        """
        # Futuro: Seleção de Backend (CPU vs CUDA)
        result_data = np.dot(a.data, b.data)
        
        # Aqui o Autograd registraria a operação no grafo
        return result_data

    @staticmethod
    def backward(ctx, grad_output):
        # Lógica de gradiente para MatMul
        pass
