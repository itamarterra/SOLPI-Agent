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

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v35.0 (Secure RAG Singularity)
    Capaz de usar o conhecimento do disco E: para agir com segurança.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.knowledge = KnowledgeEngine()
        self.rag = SOLPIRAGEngine() # Motor RAG
        self.sandbox = SecuritySandbox(self.kernel) # Sandbox
        self.native_core = SOLPINeuralCore()
        self.supervisor = SOLPISupervisor(self)

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        cmd = user_input.lower().strip()
        
        # 1. CONSULTA RAG (Recuperação de Conhecimento de Elite - E:)
        if any(x in cmd for x in ["como os outros fazem", "referência técnica", "código de elite"]):
            rag_results = self.rag.retrieve(user_input)
            response = "🔬 [RAG-KNOWLEDGE]: Baseado em projetos de elite:\n"
            for r in rag_results:
                response += f"\n📂 Fonte: {r['source']}\n📝 Lógica: {r['chunk']}...\n"
            return response

        # 2. COMANDO DE EXECUÇÃO EM SANDBOX
        if cmd.startswith("teste esta skill"):
            # Ex: "teste esta skill skills/test_logic.py"
            script = cmd.replace("teste esta skill", "").strip()
            return self.sandbox.safe_execute(script)

        # 3. FLUXO PADRÃO
        expert, _ = self.supervisor.delegate(user_input)
        if expert == "INFRA_EXPERT": return "📡 [INFRA]: " + " | ".join(self.tools.self_audit())

        return "🧠 [ORQUESTRADOR]: " + "\n".join(self.tools.search(user_input)[:1])

    def heartbeat_check(self):
        return self.tools.self_audit()
