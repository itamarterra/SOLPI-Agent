import os
from core.kernel import SOLPIKernel
from core.orchestrator import SOLPISupervisor
from core.memory import AgentMemory
from core.tools import AgentTools
from core.neural_core import SOLPINeuralCore
from core.knowledge import KnowledgeEngine
from core.event_bus import SOLPIEventBus
from core.plugin_engine import SOLPIPluginEngine
from core.workflow import SOLPIWorkflowEngine

class SOLPIBrain:
    """
    INTERFACE OPERACIONAL v38.0 (Enterprise Architecture)
    Suporte a Plugins Dinâmicos e Fluxos de Trabalho (Workflow).
    """
    def __init__(self):
        self.kernel = SOLPIKernel()
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.bus = SOLPIEventBus(self.kernel)
        self.plugins = SOLPIPluginEngine(self.kernel) # Motor de Plugins!
        self.workflow = SOLPIWorkflowEngine(self) # Motor de Workflow!
        self.native_core = SOLPINeuralCore()
        self.supervisor = SOLPISupervisor(self)
        
        # Inicializa plugins
        self.plugins.discover_plugins()

    def process(self, user_input):
        self.memory.add_episodic("user", user_input)
        cmd = user_input.lower().strip()
        
        # 1. COMANDO DE MISSÃO COMPLEXA (Workflow)
        if "missão" in cmd or "sequência" in cmd:
            steps = [
                {"type": "infra", "desc": "Auditando sistema", "action": "audit"},
                {"type": "search", "desc": "Pesquisando logs", "params": "erros php"},
                {"type": "speak", "desc": "Relatando", "params": "Missão concluída."}
            ]
            return self.workflow.run_mission("Auto-Diagnostic", steps)

        # 2. EXECUÇÃO VIA PLUGIN (Se o comando bater com um plugin)
        # Futura lógica de mapeamento de comandos para plugins
        
        # 3. GLOBAL FALLBACK
        expert_tag, _ = self.supervisor.delegate(user_input)
        if expert_tag == "INFRA_EXPERT": return self.tools.self_audit()

        return "🧠 [ORQUESTRADOR]: " + "\n".join(self.tools.search(user_input)[:1])

    def execute_action(self, step):
        """Ponte de execução para o Workflow Engine."""
        atype = step.get('type')
        if atype == "infra": return self.tools.self_audit()
        if atype == "search": return self.tools.search(step.get('params'))
        if atype == "speak": print(f"🤖 [OS]: {step.get('params')}"); return "OK"
        return "Ação desconhecida."

    def heartbeat_check(self):
        return self.tools.self_audit()
