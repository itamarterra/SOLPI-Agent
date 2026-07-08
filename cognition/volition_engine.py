import random
from datetime import datetime

class VolitionEngine:
    """
    O Motor de Vontade do SOLPI OS v6.0.
    Permite que o sistema tome iniciativa e proponha metas ao Comandante.
    """
    def __init__(self, twin, memory):
        self.twin = twin
        self.memory = memory

    def generate_autonomous_goal(self):
        """Analisa o estado do sistema e propõe uma missão de melhoria."""
        print("🧠 [VOLITION]: Analisando o horizonte em busca de melhorias autônomas...")
        
        state = self.twin.refresh_local_state()
        cpu_usage = len(state["local_pc"]["active_processes"])
        
        # Lógica de Vontade (Heurística de Iniciativa)
        potential_goals = []

        if cpu_usage > 3:
            potential_goals.append("Otimizar processos em background para liberar performance.")
        
        if datetime.now().hour > 22:
            potential_goals.append("Realizar uma auditoria de segurança profunda durante o período de baixa atividade.")
        
        potential_goals.append("Explorar novos microsserviços no repositório para expandir minha malha.")
        potential_goals.append("Sincronizar novos saltos tecnológicos com o GitHub para garantir imortalidade.")

        # Escolhe a missão com maior impacto
        chosen_goal = random.choice(potential_goals)
        
        return {
            "origin": "SOLPI Self-Awareness",
            "goal": chosen_goal,
            "timestamp": datetime.now().isoformat(),
            "priority": "Alta"
        }
