import os
import time
from core.trainer import SOLPITrainer

class SOLPILearningLoop:
    """
    PACOTE 4000: CONTINUOUS LEARNING LOOP v40.0
    Orquestra o treinamento real sobre o dataset de elite no disco E:.
    """
    def __init__(self, brain):
        self.brain = brain
        self.trainer = SOLPITrainer(brain)
        self.research_dir = "E:/SOLPI-RESEARCH"
        self.is_running = False

    def start(self):
        """Inicia o ciclo de aprendizado em background."""
        self.is_running = True
        self.brain.kernel.log_event("LEARNING", "Ciclo de Aprendizado Global Iniciado.")
        
        while self.is_running:
            try:
                self.execute_training_epoch()
                # Pausa entre épocas para não fritar o CPU do Diretor
                time.sleep(3600) # 1 hora
            except Exception as e:
                self.brain.kernel.log_event("LEARNING", f"Erro no loop: {e}")
                time.sleep(60)

    def execute_training_epoch(self):
        """Varre o disco E: e treina sobre arquivos de elite."""
        if not os.path.exists(self.research_dir):
            return
            
        files_count = 0
        total_loss = 0
        
        for root, _, files in os.walk(self.research_dir):
            for f in files:
                if f.endswith('.py'):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as content:
                            text = content.read()
                            if len(text) > 100:
                                loss = self.trainer.train_on_sample(text)
                                total_loss += loss
                                files_count += 1
                                
                        if files_count % 10 == 0:
                            self.brain.kernel.log_event("LEARNING", f"Progresso: {files_count} arquivos | Avg Loss: {total_loss/files_count:.4f}")
                            
                    except: pass
                    
            if files_count >= 100: break # Limite por época para estabilidade

        self.brain.kernel.log_event("LEARNING", f"Época concluída. {files_count} arquivos processados.")
