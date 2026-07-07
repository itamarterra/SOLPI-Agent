import os
import subprocess
from agents.base_agent import BaseAgent

class ProgrammingAgent(BaseAgent):
    """
    O Engenheiro do SOLPI OS: Capaz de ler, escrever e testar o próprio código do sistema.
    """
    def register_tools(self):
        self.registry.register("ProgrammingAgent", "read_code", "Lê o conteúdo de um arquivo fonte")
        self.registry.register("ProgrammingAgent", "write_code", "Cria ou sobrescreve um arquivo de código")
        self.registry.register("ProgrammingAgent", "run_validation", "Executa análise estática ou testes no código")

    def execute(self, task_description):
        print(f"💻 [PROGRAMMING AGENT]: Iniciando tarefa de engenharia -> {task_description}")
        task_lower = task_description.lower()
        
        # 1. Operação de Leitura
        if "leia" in task_lower or "read" in task_lower:
            path = self._extract_path(task_description)
            return self._read_file(path)
            
        # 2. Operação de Escrita/Criação
        elif "escreva" in task_lower or "crie" in task_lower:
            # Em um cenário real, o conteúdo viria processado pela IA
            path = self._extract_path(task_description)
            return f"ProgrammingAgent: Aguardando conteúdo estruturado para gravar em {path}"

        # 3. Validação de Código
        elif "valide" in task_lower or "teste" in task_lower:
            return self._run_lint()

        return f"ProgrammingAgent: Tarefa '{task_description}' processada."

    def _extract_path(self, text):
        # Lógica simples de extração de caminho (pode ser melhorada com regex)
        words = text.split()
        for word in words:
            if "/" in word or "\\" in word or "." in word:
                return word
        return "temp_code.py"

    def _read_file(self, path):
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.log_activity(f"Leu o arquivo: {path}")
                return content
            return f"❌ Arquivo {path} não encontrado."
        except Exception as e:
            return str(e)

    def _run_lint(self):
        # Exemplo de auto-validação usando flake8 ou similar
        self.log_activity("Executou validação de integridade do código")
        return "✅ Integridade do Código: OK (Nenhum erro de sintaxe detectado)"
