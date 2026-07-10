import numpy as np

class SOLPIAdamW:
    # ... (já implementado) ...
    pass

class SOLPIScheduler:
    """
    PACOTE 0905: COSINE SCHEDULER v1.0
    Ajusta o Learning Rate ao longo do tempo (Fase 14).
    """
    def __init__(self, initial_lr, max_steps):
        self.initial_lr = initial_lr
        self.max_steps = max_steps

    def get_lr(self, current_step):
        # Matemática de decaimento de cosseno
        cos_out = np.cos(np.pi * current_step / self.max_steps)
        return self.initial_lr * 0.5 * (1 + cos_out)
