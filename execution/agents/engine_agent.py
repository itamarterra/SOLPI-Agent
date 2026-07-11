import sys
import os

# Adiciona o diretório do motor de elite ao sys.path
engine_path = os.path.join(os.getcwd(), "solpi-engine")
if engine_path not in sys.path:
    sys.path.append(engine_path)

from execution.agents.base import BaseAgent
try:
    from run_agent import AIAgent
except ImportError:
    AIAgent = None

class SolpiEngineAgent(BaseAgent):
    """
    PACOTE 1604: SOLPI ENGINE AGENT v60.0 (Singularity Integration)
    Agente de elite especializado em multi-tool calling e tarefas complexas.
    """
    def __init__(self, brain):
        super().__init__(brain)
        self.engine = None
        if AIAgent:
            # Inicializa com as configurações de modelo do SOLPI
            self.engine = AIAgent(
                model=self.brain.config.MODEL_PATH,
                enabled_toolsets=["research", "development"]
            )

    def run(self, task):
        self.kernel.log_event("SOLPI_ENGINE", f"Iniciando missão complexa: {task[:30]}...")
        
        if not self.engine:
            return "❌ Motor de Elite não inicializado (Verifique dependências no drive E:)."
            
        try:
            # Executa a conversa via motor de elite
            result = self.engine.run_conversation(task)
            return result.get("final_response", "Missão concluída sem resposta textual.")
        except Exception as e:
            self.kernel.log_event("ERROR", f"Falha no Solpi Engine Agent: {e}")
            return f"❌ Falha na execução do Motor: {str(e)}"
