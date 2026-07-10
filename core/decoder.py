import numpy as np

class SOLPIDecoder:
    """
    PACOTE 1200: INFERÊNCIA v1.0
    Implementa a geração autoregressiva de tokens (Greedy Search).
    """
    def __init__(self, brain):
        self.brain = brain

    def generate(self, prompt, max_new_tokens=20):
        """Gera uma sequência de resposta token a token."""
        tokens = self.brain.native_core.tokenizer.encode(prompt)
        generated = []
        
        for _ in range(max_new_tokens):
            # 1. Obtém Logits do último token
            logits = self.brain.native_core.get_logits(tokens)
            
            # 2. Escolha Gananciosa (Greedy - Etapa 1200)
            next_token = np.argmax(logits)
            
            # 3. Condição de parada (EOS - Etapa 0308)
            if next_token == 3: # ID do <EOS>
                break
                
            generated.append(next_token)
            tokens.append(next_token)
            
        return self.brain.native_core.tokenizer.decode(generated)
