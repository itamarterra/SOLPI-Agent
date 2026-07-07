import random

class SimulationEngine:
    """
    Motor de Simulação do SOLPI OS v5.2.
    Testa o plano no 'silêncio' para prever riscos e chances de sucesso.
    """
    def __init__(self, memory, world_model):
        self.memory = memory
        self.world = world_model

    def simulate_plan(self, plan):
        """Avalia cada etapa do plano sem executá-la fisicamente."""
        print("🔮 [SIMULATION]: Rodando simulação do plano...")
        
        simulation_report = {
            "predicted_success_rate": 0.0,
            "high_risk_steps": [],
            "estimated_duration": 0.0,
            "bottlenecks": []
        }
        
        total_steps = len(plan)
        success_weights = 0
        
        for step in plan:
            # 1. Checa contra histórico de falhas na memória
            past_failures = self.memory.recall(f"falha {step['task']}", layer="experience")
            
            # 2. Avalia impacto no sistema atual (via World Model)
            current_cpu = float(self.world.state.get('resources', {}).get('cpu', '0%').replace('%', ''))
            
            step_risk = "Baixo"
            step_success_prob = 0.95
            
            if past_failures:
                step_risk = "Médio"
                step_success_prob = 0.70
                
            if current_cpu > 80:
                step_risk = "Alto"
                step_success_prob -= 0.20

            if step_risk == "Alto":
                simulation_report["high_risk_steps"].append(step['task'])
            
            success_weights += step_success_prob
            simulation_report["estimated_duration"] += 2.5 # Segundos estimados por etapa
            
        simulation_report["predicted_success_rate"] = round((success_weights / total_steps) * 100, 2)
        
        print(f"📊 [SIMULATION]: Relatório -> Sucesso Previsto: {simulation_report['predicted_success_rate']}%")
        return simulation_report
