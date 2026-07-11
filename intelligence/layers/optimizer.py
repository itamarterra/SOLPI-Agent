import numpy as np

class SOLPIAdamW:
    """
    PACOTE 0900: ADAMW OPTIMIZER v50.0 (Neural Depth)
    Implementa Adam com Weight Decay para estabilidade e performance.
    """
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.01):
        self.params = params
        self.lr = lr
        self.betas = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, params, grads):
        self.t += 1
        for i, (p, g) in enumerate(zip(params, grads)):
            if g is None: continue
            
            # Weight Decay (Regularização L2)
            p *= (1 - self.lr * self.weight_decay)
            
            # Atualiza momentos
            self.m[i] = self.betas[0] * self.m[i] + (1 - self.betas[0]) * g
            self.v[i] = self.betas[1] * self.v[i] + (1 - self.betas[1]) * (g ** 2)
            
            # Correção de viés
            m_hat = self.m[i] / (1 - self.betas[0] ** self.t)
            v_hat = self.v[i] / (1 - self.betas[1] ** self.t)
            
            # Atualização do parâmetro
            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

class SOLPICosineScheduler:
    def __init__(self, initial_lr, max_steps):
        self.initial_lr = initial_lr
        self.max_steps = max_steps

    def get_lr(self, step):
        return self.initial_lr * 0.5 * (1 + np.cos(np.pi * step / self.max_steps))
