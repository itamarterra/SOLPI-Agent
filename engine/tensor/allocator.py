import numpy as np

class SOLPITensor:
    """
    PACOTE 2100: TENSOR OBJECT v1.0
    A unidade base de computação do SOLPI.
    """
    def __init__(self, data, device="cpu", dtype="float32", requires_grad=False):
        self.data = np.array(data, dtype=dtype)
        self.device = device
        self.dtype = dtype
        self.requires_grad = requires_grad
        self.grad = None
        self.shape = self.data.shape

    def __repr__(self):
        return f"SOLPITensor({self.shape}, device={self.device}, dtype={self.dtype})"

class SOLPITensorAllocator:
    """
    PACOTE 2110: TENSOR ALLOCATOR
    Gerencia a alocação e o pool de memória de tensores.
    """
    def __init__(self):
        self.active_tensors = 0

    def allocate(self, shape, dtype="float32", device="cpu"):
        data = np.zeros(shape, dtype=dtype)
        self.active_tensors += 1
        return SOLPITensor(data, device=device, dtype=dtype)
