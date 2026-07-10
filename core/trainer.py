import time
from core.loss import SOLPICrossEntropyLoss
from core.optimizer import SOLPIAdamW

class SOLPITrainer:
    """
    PACOTE 1100: TRAINING ENGINE v1.0
    Executa o ciclo de aprendizado sobre o dataset de pesquisa.
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
        
        # Simplificando para o passo de treino (Etapa 1102-1105)
        for i in range(len(tokens)-1):
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
            # Cria lista de gradientes (um para cada parâmetro)
            # Para simplificar v40, aplicamos o gradiente principal nos embeddings e projeção
            grads = [grad if p.shape == grad.shape else np.zeros_like(p) for p in params]
            
            self.optimizer.step(params, grads)
            
        avg_loss = total_loss / len(tokens)
        
        # 4. Reflection Audit (v40.0)
        # Calcula grad_norm aproximado para auditoria
        grad_norm = np.linalg.norm(grad)
        self.brain.reflection.audit_training_step(epoch, avg_loss, grad_norm)
        
        return avg_loss
