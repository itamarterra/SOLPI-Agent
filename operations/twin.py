import time
import json

class SOLPIDigitalTwin:
    """
    PACOTE 1800: DIGITAL TWIN v50.4
    Visualização em tempo real da Plataforma SOLPI-OS.
    Migrado para o Domínio de Operações.
    """
    def __init__(self, brain):
        self.brain = brain

    def get_state(self):
        """Coleta o estado global de todos os domínios."""
        return {
            "timestamp": time.time(),
            "platform": self.brain.kernel.hardware,
            "intelligence": {
                "state": self.brain.state_manager.get_state(),
                "model": self.brain.model_registry.active_model_name
            },
            "operations": self.brain.telemetry.get_snapshot()
        }

    def export_3d(self):
        return json.dumps(self.get_state())
