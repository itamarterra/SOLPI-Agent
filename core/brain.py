import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.dataset import SOLPIDataset
from core.rag import SOLPIRAGEngine
from core.security import SecuritySandbox
from core.experts import InfraExpert, DevExpert, KnowledgeExpert, SQLExpert
from core.context_manager import SOLPIContextManager
from core.sampler import SOLPISampler

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v36.0 (Context & SQL Singularity)
    Capaz de diálogos longos e consultas diretas ao banco de ativos.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.knowledge = KnowledgeEngine()
        self.rag = SOLPIRAGEngine()
        self.sandbox = SecuritySandbox(self.kernel)
        self.context = SOLPIContextManager() # Novo!
        self.native_core = SOLPINeuralCore()
        self.supervisor = SOLPISupervisor(self)
        
        # Especialistas
        self.sql_expert = SQLExpert(self) # Novo!

    def process(self, user_input):
        self.context.add_to_context("user", user_input)
        cmd = user_input.lower().strip()
        
        # 1. DELEGAÇÃO PARA SQL (Ativos/Banco)
        if any(x in cmd for x in ["lista", "computadores", "ativos", "banco", "database"]):
            return self.sql_expert.run(user_input)

        # 2. FLUXO PADRÃO COM CONTEXTO (Etapa 1307)
        expert, _ = self.supervisor.delegate(user_input)
        if expert == "INFRA_EXPERT": return "📡 [INFRA]: " + " | ".join(self.tools.self_audit())

        # 3. PESQUISA WEB (Fallback)
        results = self.tools.search(user_input)
        response = "🧠 [GLOBAL]: " + "\n".join(results[:1])
        self.context.add_to_context("assistant", response)
        return response

    def heartbeat_check(self):
        return self.tools.self_audit()
