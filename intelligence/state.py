class SOLPIStateManager:
    """
    PACOTE 9100: STATE MANAGER v1.0
    Controla o estado global do SOLPI-OS (Idle, Thinking, Learning, etc).
    Essencial para a observabilidade do Digital Twin.
    """
    IDLE = "IDLE"
    THINKING = "THINKING"
    LEARNING = "LEARNING"
    EXECUTING = "EXECUTING"
    RECOVERING = "RECOVERING"

    def __init__(self, brain):
        self.brain = brain
        self.current_state = self.IDLE

    def transition_to(self, new_state):
        if self.current_state != new_state:
            old_state = self.current_state
            self.current_state = new_state
            self.brain.kernel.log_event("STATE", f"Transição: {old_state} -> {new_state}")
            # Publica a mudança para o Twin e Telemetria
            self.brain.event_bus.publish("state_changed", {"from": old_state, "to": new_state})

    def get_state(self):
        return self.current_state
