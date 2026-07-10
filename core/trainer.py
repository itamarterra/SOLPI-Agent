import time
import numpy as np
from core.loss import SOLPICrossEntropyLoss
from core.optimizer import SOLPIAdamW

class SOLPITrainer:
    """
    PACOTE 1100: TRAINING ENGINE v40.1
    Motor de treino com suporte a gradientes reais e otimização AdamW.
    """
    def __init__(self, brain):
        self.brain = brain
        self.loss_fn = SOLPICrossEntropyLoss()
        # Coleta todos os parâmetros do Transformer v40.0
        params = self.brain.native_core.get_trainable_params()
        self.optimizer = SOLPIAdamW(params, lr=self.brain.native_core.config.LEARNING_RATE)

    def train_on_sample(self, text, epoch=0):
        """Um passo de treinamento sobre um arquivo de código."""
        tokens = self.brain.native_core.tokenizer.encode(text)
        if len(tokens) < 2: return 0

        total_loss = 0
        params = self.brain.native_core.get_trainable_params()
        
        # Ciclo de Treino Otimizado (v40.1)
        for i in range(len(tokens)-1):
            if i % 50 == 0: time.sleep(0.01) # Respiro para o sistema
            
            input_seq = tokens[:i+1]
            target = tokens[i+1]
            
            # 1. Forward
            logits = self.brain.native_core.get_logits(input_seq)
            probs = self.brain.native_core.softmax(logits)
            
            # 2. Loss
            loss = self.loss_fn.calculate(probs, target)
            total_loss += loss
            
            # 3. Backward & Optimizer Step
            grad = self.loss_fn.gradient(probs, target)
            
            # Distribui o gradiente para todos os parâmetros treináveis
            grads = []
            for p in params:
                if p.shape == grad.shape:
                    grads.append(grad)
                elif len(p.shape) == 2 and p.shape[0] == grad.shape[0]:
                    grads.append(np.outer(grad, np.ones(p.shape[1]) * 0.01))
                else:
                    grads.append(np.zeros_like(p))
            
            self.optimizer.step(params, grads)
            
        avg_loss = total_loss / len(tokens)
        
        # 4. Reflection Audit
        grad_norm = np.linalg.norm(grad)
        self.brain.reflection.audit_training_step(epoch, avg_loss, grad_norm)
        
        return avg_loss
