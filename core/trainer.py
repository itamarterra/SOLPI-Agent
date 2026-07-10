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
        # Coleta parâmetros do Transformer para o AdamW
        params = [self.brain.native_core.embeddings] 
        self.optimizer = SOLPIAdamW(params, lr=self.brain.native_core.config.LEARNING_RATE)

    def train_on_sample(self, text):
        """Um passo de treinamento sobre um arquivo de código."""
        tokens = self.brain.native_core.tokenizer.encode(text)
        if len(tokens) < 2: return 0

        total_loss = 0
        # Simplificando para o passo de treino (Etapa 1102-1105)
        for i in range(len(tokens)-1):
            input_seq = tokens[:i+1]
            target = tokens[i+1]
            
            # 1. Forward (Neural Core)
            # Retorna logits da última posição
            logits = self.brain.native_core.get_logits(input_seq)
            probs = self.brain.native_core.softmax(logits)
            
            # 2. Loss
            loss = self.loss_fn.calculate(probs, target)
            total_loss += loss
            
            # 3. Backward & Optimizer Step
            grad = self.loss_fn.gradient(probs, target)
            # Atualiza apenas embeddings por enquanto para estabilidade
            self.optimizer.step([self.brain.native_core.embeddings], [grad])
            
        return total_loss / len(tokens)
