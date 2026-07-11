from execution.agents.base import BaseAgent

class DevAgent(BaseAgent):
    """
    PACOTE 1601: DEV AGENT v50.0
    Especialista em Engenharia de Software e Refatoração.
    """
    def run(self, task):
        # Visão se necessário
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
