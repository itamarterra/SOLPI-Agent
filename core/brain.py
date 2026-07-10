import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.dataset import SOLPIDataset
from core.trainer import SOLPITrainer
from core.decoder import SOLPIDecoder
from core.researcher import SOLPIResearcher
from core.experts import InfraExpert, DevExpert, KnowledgeExpert

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v34.0 (Full Expert Orchestration)
    Arquitetura com Agentes Reais e Geração Autoregressiva.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.knowledge = KnowledgeEngine()
        self.researcher = SOLPIResearcher()
        self.native_core = SOLPINeuralCore()
        self.supervisor = SOLPISupervisor(self)
        self.dataset = SOLPIDataset()
        
        # Motores e Especialistas
        self.trainer = SOLPITrainer(self)
        self.decoder = SOLPIDecoder(self)
        self.infra_expert = InfraExpert(self)
        self.dev_expert = DevExpert(self)
        self.kn_expert = KnowledgeExpert(self)

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        cmd = user_input.lower().strip()
        
        # 1. DELEGAÇÃO PELO SUPERVISOR
        expert_tag, mission = self.supervisor.delegate(user_input)
        print(f"👮 [SUPERVISOR]: Delegando para {expert_tag}")

        # 2. EXECUÇÃO POR OBJETO ESPECIALISTA (Fase 16)
        if expert_tag == "INFRA_EXPERT":
            response = self.infra_expert.run()
        elif expert_tag == "DEV_EXPERT":
            response = self.dev_expert.run(user_input)
        elif expert_tag == "KNOWLEDGE_EXPERT":
            response = self.kn_expert.run(user_input)
        else:
            # 3. GERAÇÃO AUTOREGRESSIVA (Fase 12)
            response = self.decoder.generate(user_input)

        self.memory.add_episodic("assistant", response)
        return response

    def heartbeat_check(self):
        return self.tools.self_audit()
