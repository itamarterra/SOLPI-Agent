import numpy as np

class Tensor:
    """
    PACOTE 0200: AUTOGRAD v2.0
    Suporte expandido para MatMul e Transpose.
    """
    def __init__(self, data, requires_grad=False, creators=None, creation_op=None):
        self.data = np.array(data)
        self.grad = None
        if requires_grad:
            self.grad = np.zeros_like(self.data)
        self.creators = creators
        self.creation_op = creation_op
        self.children = {}

    def backward(self, grad=None):
        if grad is None: grad = np.ones_like(self.data)
        self.grad = grad

        if self.creation_op == "add":
            for c in self.creators: c.backward(grad)
            
        if self.creation_op == "matmul":
            # d(XW)/dX = dW^T, d(XW)/dW = dX^T
            self.creators[0].backward(np.dot(grad, self.creators[1].data.T))
            self.creators[1].backward(np.dot(self.creators[0].data.T, grad))

    def __add__(self, other):
        return Tensor(self.data + other.data, requires_grad=True, creators=[self, other], creation_op="add")

    def matmul(self, other):
        """Multiplicação de Matrizes com Gradiente."""
        return Tensor(np.dot(self.data, other.data), requires_grad=True, creators=[self, other], creation_op="matmul")

    def T(self):
        """Transposta."""
        return Tensor(self.data.T, requires_grad=self.grad is not None)
