import importlib
import os

class Executor:
    """
    O Gerente de Execução do SOLPI-AIOS.
    Instancia agentes e delega tarefas conforme o plano.
    """
    def __init__(self, memory, registry=None):
        self.memory = memory
        self.registry = registry
        self.active_agents = {}

    def run_plan(self, plan):
        """Executa a sequência de tarefas chamando os agentes necessários."""
        final_results = []
        
        for step in plan:
            agent_name = step['agent']
            task = step['task']
            
            print(f"⚡ [EXECUTOR]: Solicitando ao {agent_name} -> {task}")
            
            # Instancia o agente dinamicamente se ainda não existir
            agent = self._get_agent(agent_name)
            
            if agent:
                try:
                    # O executor passa a tarefa para o agente
                    result = agent.execute(task)
                    final_results.append(result)
                except Exception as e:
                    print(f"❌ [EXECUTOR]: Erro no agente {agent_name}: {e}")
                    final_results.append(f"Erro: {str(e)}")
            else:
                print(f"⚠️ [EXECUTOR]: Agente {agent_name} não encontrado ou não implementado.")
                final_results.append("Agente indisponível")
                
        return "\n".join([str(r) for r in final_results])

    def _get_agent(self, agent_name):
        """Carrega e instancia o agente da pasta /agents."""
        if agent_name in self.active_agents:
            return self.active_agents[agent_name]

        # Converte CamelCase para snake_case para achar o arquivo (Ex: WindowsAgent -> windows_agent)
        import re
        file_name = re.sub(r'(?<!^)(?=[A-Z])', '_', agent_name).lower()
        
        try:
            module = importlib.import_module(f"agents.{file_name}")
            agent_class = getattr(module, agent_name)
            instance = agent_class(self.memory, self.registry)
            self.active_agents[agent_name] = instance
            return instance
        except Exception as e:
            # Fallback para agentes não criados ainda
            return None
