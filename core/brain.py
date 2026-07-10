import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.dataset import SOLPIDataset
from core.trainer import SOLPITrainer

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v33.0 (Self-Training Singularity)
    Primeira versão com ciclo de aprendizado Backprop real.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.knowledge = KnowledgeEngine()
        self.native_core = SOLPINeuralCore()
        self.supervisor = SOLPISupervisor(self)
        self.dataset = SOLPIDataset()
        self.trainer = SOLPITrainer(self) # Motor de Treino!

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        cmd = user_input.lower().strip()
        
        # 1. COMANDO DE EVOLUÇÃO REAL (Fase 11)
        if any(x in cmd for x in ["treinar", "iniciar evolução", "aprenda com a pesquisa"]):
            return self.run_deep_learning()

        # 2. FLUXO PADRÃO (Supervisão + Especialistas)
        expert, mission = self.supervisor.delegate(user_input)
        
        if expert == "INFRA_EXPERT":
            return "📡 [INFRA]: " + "\n- ".join(self.tools.self_audit())

        return "🧠 [ORQUESTRADOR]: " + "\n".join(self.tools.search(user_input)[:1])

    def run_deep_learning(self):
        """O Agente estuda o código do disco E: e ajusta seus pesos reais."""
        self.kernel.log_event("TRAINING", "Iniciando Deep Learning Ciclo 1.")
        
        batch = self.dataset.get_batch(size=3)
        for i, code in enumerate(batch):
            loss = self.trainer.train_on_sample(code)
            print(f"📉 [EPOCH {i+1}]: Loss = {loss:.4f}")
            
        self.native_core.save_weights() # Salva a inteligência adquirida
        return f"✅ Evolução v33.0 concluída. Pesos atualizados com base em código de elite."
