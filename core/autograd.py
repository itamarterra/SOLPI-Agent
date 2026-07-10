import numpy as np

class Tensor:
    """
    PACOTE 0200: AUTOGRAD v1.0
    Tensor com suporte a Grafo Computacional e Backpropagation.
    """
    def __init__(self, data, requires_grad=False, creators=None, creation_op=None):
        self.data = np.array(data)
        self.grad = None
        if requires_grad:
            self.grad = np.zeros_like(self.data)
        self.creators = creators
        self.creation_op = creation_op
        self.children = {}

        if creators is not None:
            for c in creators:
                if self.__hash__() not in c.children:
                    c.children[self.__hash__()] = 1
                else:
                    c.children[self.__hash__()] += 1

    def backward(self, grad=None):
        """Etapa 0201: Backpropagation real."""
        if grad is None:
            grad = np.ones_like(self.data)
        
        self.grad = grad

        if self.creation_op == "add":
            self.creators[0].backward(grad)
            self.creators[1].backward(grad)
            
        if self.creation_op == "mul":
            new_grad_0 = grad * self.creators[1].data
            new_grad_1 = grad * self.creators[0].data
            self.creators[0].backward(new_grad_0)
            self.creators[1].backward(new_grad_1)

    def __add__(self, other):
        return Tensor(self.data + other.data, requires_grad=True, creators=[self, other], creation_op="add")

    def __mul__(self, other):
        return Tensor(self.data * other.data, requires_grad=True, creators=[self, other], creation_op="mul")

    def __repr__(self):
        return str(self.data)
