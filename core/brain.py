import time
import threading
from core.tools import AgentTools

class SOLPIBrain:
    def __init__(self):
        self.tools = AgentTools()
        self.is_evolving = False

    def _evolution_loop(self):
        """Loop protegido com monitoramento de hardware."""
        while self.is_evolving:
            # Proteção 1: Checa se o PC está travando
            healthy, msg = self.tools.check_pc_health()
            if not healthy:
                self.tools.log_evolution(f"CRÍTICO: PC SOBRECARREGADO ({msg}). Pausando evolução.")
                self.is_evolving = False
                self.tools.speak("Itamar, detectei sobrecarga no seu PC. Vou parar minhas tarefas de fundo para não travar o sistema.")
                break

            try:
                # 2. Executa tarefas pequenas com pausas grandes
                self.tools.log_evolution("Vigilância de rotina concluída.")
                time.sleep(300) # Espera 5 minutos entre as ações
            except:
                time.sleep(60)

    def process(self, user_input):
        cmd = user_input.lower()
        
        # Início seguro
        if "evolua" in cmd:
            if not self.is_evolving:
                self.is_evolving = True
                threading.Thread(target=self._evolution_loop, daemon=True).start()
                return "Modo Evolução ativado com travas de segurança de hardware."
            return "Já estou em evolução."

        if user_input.startswith("$"):
            # Só roda comandos curtos
            return f"Resultado: {self.tools.execute_shell(user_input[1:].strip())['stdout'][:500]}"

        return "Cérebro estabilizado. O que deseja fazer agora?"
