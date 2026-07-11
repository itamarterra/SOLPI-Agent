import sys
import os

# Adiciona o diretório do Hermes ao sys.path para permitir importações internas dele
hermes_path = os.path.join(os.getcwd(), "hermes-core")
if hermes_path not in sys.path:
    sys.path.append(hermes_path)

from execution.agents.base import BaseAgent
try:
    from run_agent import AIAgent
except ImportError:
    AIAgent = None

class HermesAgent(BaseAgent):
    """
    PACOTE 1604: HERMES AGENT v50.0 (Singularity Integration)
    Agente de elite integrado a partir do projeto Hermes.
    Especializado em multi-tool calling, navegação e tarefas complexas.
    """
    def __init__(self, brain):
        super().__init__(brain)
        self.hermes_engine = None
        if AIAgent:
            # Inicializa com as configurações de modelo do SOLPI
            self.hermes_engine = AIAgent(
                model=self.brain.config.MODEL_PATH,
                enabled_toolsets=["research", "development"]
            )

    def run(self, task):
        self.kernel.log_event("HERMES", f"Iniciando missão complexa: {task[:30]}...")
        
        if not self.hermes_engine:
            return "❌ Hermes Engine não inicializada (Verifique dependências no drive E:)."
            
        try:
            # Executa a conversa via motor do Hermes
            result = self.hermes_engine.run_conversation(task)
            return result.get("final_response", "Missão concluída sem resposta textual.")
        except Exception as e:
            self.kernel.log_event("ERROR", f"Falha no Hermes Agent: {e}")
            return f"❌ Falha na execução Hermes: {str(e)}"
