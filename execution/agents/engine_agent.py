import sys
import os
import json

# Adiciona o diretório do motor de elite ao sys.path
engine_path = os.path.join(os.getcwd(), "solpi-engine")
if engine_path not in sys.path:
    sys.path.append(engine_path)

from execution.agents.base import BaseAgent
try:
    from run_agent import AIAgent
    import model_tools
except ImportError:
    AIAgent = None
    model_tools = None

class SolpiEngineAgent(BaseAgent):
    """
    PACOTE 1604: SOLPI ENGINE AGENT v70.6 (Elite Integration)
    Agente de elite que atua como ponte para o motor SOLPI-ENGINE (ex-Hermes).
    Responsável por executar ferramentas de baixo nível (Terminal, Browser, etc).
    """
    def __init__(self, brain):
        super().__init__(brain)
        self.engine = None
        if AIAgent:
            # Inicializa o motor
            # Ele vai ler automaticamente do config.yaml
            self.engine = AIAgent(
                enabled_toolsets=["web", "terminal"]
            )

    def run(self, task):
        self.kernel.log_event("SOLPI_ENGINE", f"Iniciando missão complexa: {task[:30]}...")
        
        if not self.engine:
            return "❌ Motor de Elite não inicializado. Verifique dependências."
            
        try:
            # Executa o loop de pensamento e uso de ferramentas do motor de elite
            result = self.engine.run_conversation(task)
            return result.get("final_response", "Tarefa concluída.")
        except Exception as e:
            self.kernel.log_event("ERROR", f"Falha no Solpi Engine: {e}")
            return f"❌ Falha na execução: {str(e)}"

    def execute_tool(self, tool_name, args):
        """Executa uma ferramenta específica do motor de elite diretamente."""
        if not model_tools:
            return "❌ Model Tools não disponível."
            
        self.kernel.log_event("ENGINE_TOOL", f"Executando ferramenta: {tool_name}")
        try:
            # Usa o dispatcher do motor de elite para rodar a ferramenta
            result = model_tools.handle_function_call(
                function_name=tool_name,
                function_args=args,
                task_id=self.brain.kernel.version
            )
            return result
        except Exception as e:
            return f"❌ Erro na ferramenta {tool_name}: {e}"

    def get_available_tools(self):
        """Retorna a lista de todas as ferramentas integradas do motor de elite."""
        if not model_tools: return []
        return model_tools.get_all_tool_names()
