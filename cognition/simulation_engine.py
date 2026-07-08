from cognition.digital_twin import DigitalTwin

class SimulationEngine:
    """
    Motor de Simulação Avançada v6.0.
    Utiliza o Gêmeo Digital para prever falhas físicas e lógicas antes da execução.
    """
    def __init__(self, memory, world_model):
        self.memory = memory
        self.world = world_model
        self.twin = DigitalTwin(memory)

    def simulate_plan(self, plan):
        """Avalia cada etapa do plano usando o Espelhamento do Gêmeo Digital."""
        print("🔮 [SIMULATION]: Rodando simulação via Digital Twin...")
        
        # Sincroniza o estado atual do PC antes da simulação
        self.twin.refresh_local_state()
        
        simulation_report = {
            "predicted_success_rate": 0.0,
            "high_risk_steps": [],
            "warnings": [],
            "estimated_duration": 0.0,
            "is_safe": True
        }
        
        total_steps = len(plan)
        if total_steps == 0: return simulation_report

        success_weights = 0
        
        for step in plan:
            # 1. Simulação no Gêmeo Digital
            prediction = self.twin.simulate_action(step['agent'], step['task'])
            
            if not prediction["safe"]:
                simulation_report["is_safe"] = False
                simulation_report["high_risk_steps"].append(step['task'])
            
            if prediction["warnings"]:
                simulation_report["warnings"].extend(prediction["warnings"])

            # 2. Ajuste de Probabilidade de Sucesso
            step_success_prob = 1.0 - (prediction["risk_score"] / 100)
            success_weights += step_success_prob
            
            simulation_report["estimated_duration"] += 1.5 
            
        simulation_report["predicted_success_rate"] = round((success_weights / total_steps) * 100, 2)
        
        print(f"📊 [SIMULATION]: Relatório Final -> Segurança: {'OK' if simulation_report['is_safe'] else 'CRÍTICA'} | Sucesso: {simulation_report['predicted_success_rate']}%")
        return simulation_report
