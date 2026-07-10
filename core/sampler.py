import numpy as np

class SOLPISampler:
    """
    PACOTE 1202/1203: SAMPLING ENGINE v1.0
    Implementa Top-K e Top-P para respostas mais naturais.
    """
    @staticmethod
    def top_k_sampling(logits, k=50):
        """Etapa 1202: Filtra os K tokens mais prováveis."""
        indices_to_remove = logits < np.partition(logits, -k)[-k]
        logits[indices_to_remove] = -float('Inf')
        return logits

    @staticmethod
    def top_p_sampling(logits, p=0.9):
        """Etapa 1203: Nucleus Sampling (Filtra tokens que somam prob P)."""
        sorted_indices = np.argsort(logits)[::-1]
        sorted_logits = logits[sorted_indices]
        
        # Calcula probabilidades acumuladas
        probs = np.exp(sorted_logits) / np.sum(np.exp(sorted_logits))
        cum_probs = np.cumsum(probs)
        
        # Remove tokens fora do núcleo P
        sorted_indices_to_remove = cum_probs > p
        # Garante que o primeiro token (mais provável) nunca seja removido
        sorted_indices_to_remove[1:] = sorted_indices_to_remove[:-1]
        sorted_indices_to_remove[0] = False
        
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = -float('Inf')
        return logits
