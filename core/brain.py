import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.researcher import SOLPIResearcher

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v32.0 (Research & Speed)
    Integra KV Cache e Explorador de Código de Elite do Disco E:.
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.knowledge = KnowledgeEngine()
        self.researcher = SOLPIResearcher() # Novo!
        self.native_core = SOLPINeuralCore()

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        cmd = user_input.lower().strip()
        
        # 1. PENSAMENTO COM KV CACHE (Fase 18)
        thought = self.native_core.think_native(user_input)
        print(f"\n{thought}")

        # 2. COMANDO DE PESQUISA TÉCNICA (Fase 23)
        if any(x in cmd for x in ["como os outros fazem", "procure no código", "exemplo de"]):
            examples = self.researcher.scan_for_patterns(user_input)
            return "🔬 [RESEARCH]: Encontrei exemplos reais nos repositórios de elite:\n- " + "\n- ".join(examples)

        # 3. COMANDOS DE INFRA/SAÚDE
        if any(x in cmd for x in ["status", "saúde", "check-up"]):
            return "📡 [OS-STATUS]:\n- " + "\n- ".join(self.tools.self_audit())

        # 4. PESQUISA WEB (Fallback)
        results = self.tools.search(user_input)
        return "🧠 [GLOBAL]: " + "\n".join(results[:2])

    def heartbeat_check(self):
        return self.tools.self_audit()
