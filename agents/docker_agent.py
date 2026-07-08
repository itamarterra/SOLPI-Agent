import subprocess
from agents.base_agent import BaseAgent

class DockerAgent(BaseAgent):
    """
    Agente especialista em orquestração de containers (Docker e Docker Compose).
    """
    def register_tools(self):
        if self.registry:
            self.registry.register(
                "DockerAgent", "list_containers", 
                "Lista todos os containers ativos no sistema"
            )
            self.registry.register(
                "DockerAgent", "compose_up", 
                "Sobe serviços definidos em um arquivo docker-compose.yml",
                {"path": "Caminho do arquivo"}
            )
            self.registry.register(
                "DockerAgent", "container_logs", 
                "Extrai os últimos logs de um container específico",
                {"name": "Nome do container"}
            )

    def execute(self, task_description):
        print(f"🐳 [DOCKER AGENT]: Operando -> {task_description}")
        task_lower = task_description.lower()

        if "lista" in task_lower or "containers" in task_lower:
            return self._run_docker_cmd("docker ps --format \"table {{.Names}}\t{{.Status}}\"")
            
        elif "compose" in task_lower and ("subir" in task_lower or "up" in task_lower):
            # Procura por caminhos no SOLPI
            path = "C:/SOLPI/glpi/docker-compose.yml" if "glpi" in task_lower else "C:/SOLPI/docker-compose.yml"
            return self._run_docker_cmd(f"docker-compose -f {path} up -d")

        elif "log" in task_lower:
            name = task_description.split("do")[-1].strip()
            return self._run_docker_cmd(f"docker logs --tail 20 {name}")

        return f"DockerAgent: Tarefa '{task_description}' processada."

    def _run_docker_cmd(self, command):
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=45
            )
            self.log_activity(f"Executou: {command}")
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Erro Docker: {str(e)}"
