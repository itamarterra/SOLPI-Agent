import time
import json

class SOLPIDigitalTwin:
    """
    PACOTE 1800: DIGITAL TWIN v40.0
    Representação virtual 3D em tempo real do ecossistema SOLPI.
    Agrega dados de Infraestrutura, Neurais e Operacionais.
    """
    def __init__(self, brain):
        self.brain = brain
        self.state = {
            "nodes": [],
            "links": [],
            "neural_activity": 0.0,
            "infra_status": "HEALTHY"
        }

    def sync(self):
        """Sincroniza o estado atual para exportação 3D."""
        stats = self.brain.telemetry.get_stats()
        reflection = self.brain.reflection.audit_log[-1] if self.brain.reflection.audit_log else {}
        
        self.state = {
            "timestamp": time.time(),
            "metrics": {
                "cpu": stats.get("cpu_usage"),
                "ram": stats.get("ram_usage"),
                "neural_load": float(stats.get("total_tokens", 0) % 100) / 100.0
            },
            "neural_core": {
                "confidence": reflection.get("confidence", 1.0),
                "entropy": reflection.get("entropy", 0.0),
                "active_experts": list(self.brain.native_core.moe.routing_stats.values())
            },
            "topology": [
                {"id": "Kernel", "val": 10},
                {"id": "NeuralCore", "val": 8},
                {"id": "MoE_Expert_0", "val": 5},
                {"id": "MoE_Expert_1", "val": 5},
                {"id": "MoE_Expert_2", "val": 5},
                {"id": "MoE_Expert_3", "val": 5},
                {"id": "RAG_Engine", "val": 6}
            ]
        }
        return self.state

    def get_3d_payload(self):
        """Retorna o payload formatado para uma engine 3D (Three.js/Unity)."""
        return json.dumps(self.sync())
