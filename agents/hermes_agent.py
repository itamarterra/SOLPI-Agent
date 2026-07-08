import os
import sys
import json
from agents.base_agent import BaseAgent

class HermesAgent(BaseAgent):
    """
    Agente de Alta Performance: Ponte de integração com o motor Hermes-Agent.
    Permite ao SOLPI OS utilizar o loop agêntico avançado do Hermes.
    """
    def __init__(self, memory, registry=None):
        # Adiciona o diretório do Hermes ao path do sistema para permitir imports internos dele
        self.hermes_path = os.path.abspath("hermes-core")
        if self.hermes_path not in sys.path:
            sys.path.append(self.hermes_path)
            
        super().__init__(memory, registry)

    def register_tools(self):
        self.registry.register(
            "HermesAgent", "advanced_solve", 
            "Resolve objetivos complexos usando o loop agêntico do Hermes (Auto-aperfeiçoamento e Tool-calling profundo)",
            {"query": "O objetivo complexo a ser resolvido"}
        )

    def execute(self, task_description):
        print(f"🏛️ [HERMES AGENT]: Assumindo controle de alta performance -> {task_description}")
        
        try:
            from run_agent import AIAgent
            
            # Inicializa o agente Hermes usando as configurações do SOLPI .env
            agent = AIAgent(
                model=os.getenv("LLM_MODEL", "gpt-4o"),
                api_key=os.getenv("LLM_API_KEY"),
                save_trajectories=True
            )
            
            # Roda a conversação no estilo Hermes
            result = agent.run_conversation(task_description)
            
            response = result.get("final_response", "Objetivo processado pelo Hermes.")
            self.log_activity(f"Hermes executou tarefa: {task_description[:50]}...")
            
            return response
        except Exception as e:
            return f"❌ Erro na ponte Hermes: {str(e)}"
