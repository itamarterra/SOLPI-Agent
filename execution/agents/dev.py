from execution.agents.base import BaseAgent

class DevAgent(BaseAgent):
    """
    PACOTE 1601: DEV AGENT v50.0
    Especialista em Engenharia de Software e Refatoração.
    """
    def run(self, task):
        # 🟢 UPGRADE v70.5: Se a tarefa for complexa, delega para o motor solpi-engine
        if len(task.split()) > 10 or any(x in task.lower() for x in ["projeto", "arquitetura", "refatorar"]):
            self.kernel.log_event("DEV", "Tarefa complexa detectada. Acionando motor solpi-engine de Engenharia.")
            return self.brain.solpi-engine_agent.run(task)

        # Caso contrário, mantém o fluxo leve nativo
        vision_info = ""
        if any(x in task.lower() for x in ["tela", "veja"]):
            vision_info = self.brain.tools.analyze_screen()
            
        # Busca no Research Drive E:
        patterns = self.brain.evolution.researcher.scan_for_patterns(task)
        
        res = [f"💻 [DEV-ENGINEERING]: {vision_info}"]
        res.append(f"Análise de padrões para: '{task}'")
        if patterns:
            res.append(f"📚 Referências de elite encontradas: {len(patterns)}")
            
        return "\n".join(res)
