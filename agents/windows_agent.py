import subprocess
import os
from agents.base_agent import BaseAgent
from core.security import SecurityGatekeeper

class WindowsAgent(BaseAgent):
    """
    Agente especializado em controle do Microsoft Windows.
    """
    def register_tools(self):
        self.tools = {
            "shell": "Executar comandos no CMD/PowerShell",
            "info": "Obter informações do sistema",
            "process": "Listar processos ativos"
        }

    def execute(self, task_description):
        print(f"🪟 [WINDOWS AGENT]: Analisando tarefa -> {task_description}")
        
        # Lógica de decisão baseada em palavras-chave (futuramente via IA)
        if "verificar" in task_description.lower() or "info" in task_description.lower():
            return self._get_system_info()
        
        # Execução de comando se houver algo específico no texto
        # Ex: "Rodar comando dir"
        if "comando" in task_description.lower():
            cmd = task_description.split("comando")[-1].strip()
            return self._run_shell(cmd)
            
        return f"WindowsAgent: Tarefa '{task_description}' processada sem comandos diretos."

    def _run_shell(self, command):
        # Usa o Guardião de Segurança que criamos antes
        safe, reason = SecurityGatekeeper.is_safe(command)
        if not safe:
            return f"ERRO: {reason}"

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            self.log_activity(f"Executou shell: {command}")
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e)

    def _get_system_info(self):
        try:
            import platform
            info = f"Sistema: {platform.system()} {platform.release()}"
            self.log_activity("Coletou informações do sistema")
            return info
        except:
            return "Indisponível"
