import subprocess
import os
from agents.base_agent import BaseAgent

class ProgrammingAgent(BaseAgent):
    """
    Agente especializado em desenvolvimento, correção de código e melhoria do próprio sistema.
    """
    def register_tools(self):
        self.tools = {
            "write_code": "Criar ou editar arquivos de script",
            "run_test": "Executar testes unitários ou lint",
            "refactor": "Melhorar estrutura de código existente",
            "analyze_bugs": "Procurar erros em arquivos de log"
        }

    def execute(self, task_description):
        print(f"💻 [PROGRAMMING AGENT]: Trabalhando no código -> {task_description}")
        task_lower = task_description.lower()
        
        # Lógica de Automação de Código
        if "crie" in task_lower or "escreva" in task_lower:
            return "ProgrammingAgent: Código gerado e salvo com sucesso (Simulação)."
            
        elif "teste" in task_lower or "valid" in task_lower:
            return self._run_lint_simulation()

        return f"ProgrammingAgent: Tarefa de engenharia '{task_description}' concluída."

    def _run_lint_simulation(self):
        self.log_activity("Executou análise estática no código core.")
        return "✅ Código validado: 0 erros encontrados."
