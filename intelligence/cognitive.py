import time

class SOLPICognitiveEngine:
    """
    PACOTE 5100: COGNITIVE ENGINE v50.7 (Singularity Phase)
    O "Gestor de Consciência" do SOLPI-OS. 
    Coordena Percepção, Atenção e Funções Executivas.
    """
    def __init__(self, brain):
        self.brain = brain
        self.goals = [
            {"id": "G1", "desc": "Manter integridade do SOLPI-OS", "priority": 1},
            {"id": "G2", "desc": "Automatizar o GLPI do Itamar", "priority": 2},
            {"id": "G3", "desc": "Evoluir o motor neural nativo", "priority": 3}
        ]
        self.active_goal = None

    def perceive_and_decide(self, user_input=None):
        """O loop de percepção: analisa o estado do mundo e decide a ação."""
        state = self.brain.state_manager.get_state()
        hardware = self.brain.kernel.hardware
        
        self.brain.kernel.log_event("COGNITION", f"Estado: {state} | Analisando prioridades...")
        
        # 1. Se não houver entrada do usuário, o sistema pensa proativamente
        if not user_input:
            return self._proactive_thought()
            
        # 2. Decide qual meta o usuário está ajudando a cumprir
        self.active_goal = self.goals[1] # Default: Automatizar GLPI
        
        return f"🧠 [COGNITION]: Focado na Meta '{self.active_goal['desc']}'."

    def _proactive_thought(self):
        """Pensamento autônomo do sistema em background."""
        # Se o disco estiver quase cheio (predição), muda a prioridade
        prediction = self.brain.predictor.analyze_trends()
        if prediction:
            self.active_goal = self.goals[0]
            return f"🚨 [AUTONOMY]: Detectei risco de falha. Priorizando Meta '{self.active_goal['desc']}'."
            
        return "🧬 [COGNITION]: Em estado contemplativo. Aprendizado contínuo ativo."
