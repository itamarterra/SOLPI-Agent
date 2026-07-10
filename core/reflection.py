import numpy as np
import datetime
import json
import os

class SOLPIReflectionEngine:
    """
    PACOTE 1500: REFLECTION ENGINE v40.0
    Sistema de Auto-Auditoria e Avaliação de Integridade Neural.
    Responsável por detectar alucinações, monitorar entropia e ajustar o foco do treinamento.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.audit_log = []
        self.history_path = "logs/reflection_history.jsonl"
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def audit_thought(self, input_text, output_tokens, confidence_scores):
        """Avalia a qualidade de um pensamento gerado."""
        avg_confidence = np.mean(confidence_scores)
        entropy = -np.sum(confidence_scores * np.log(confidence_scores + 1e-9))
        
        reflection = {
            "timestamp": datetime.datetime.now().isoformat(),
            "input_preview": input_text[:50],
            "confidence": float(avg_confidence),
            "entropy": float(entropy),
            "status": "VALID" if avg_confidence > 0.7 else "LOW_CONFIDENCE"
        }
        
        if reflection["status"] == "LOW_CONFIDENCE":
            self.kernel.log_event("REFLECTION", f"⚠️ Alerta: Baixa confiança ({avg_confidence:.2f})")
            # Trigger de reforço: Marcar para re-treinamento
            self.kernel.event_bus.publish("neural_anomaly", reflection)

        self._persist(reflection)
        return reflection

    def audit_training_step(self, epoch, loss, gradient_norm):
        """Monitora a saúde do processo de treinamento."""
        status = "STABLE"
        if loss > 10.0: status = "DIVERGING"
        if gradient_norm < 1e-7: status = "VANISHING_GRADIENT"
        
        audit_entry = {
            "type": "training_audit",
            "epoch": epoch,
            "loss": float(loss),
            "grad_norm": float(gradient_norm),
            "status": status
        }
        
        if status != "STABLE":
            self.kernel.log_event("TRAINING", f"🚨 Crise Neural no Treino: {status} (Loss: {loss:.4f})")
            self.kernel.event_bus.publish("training_anomaly", audit_entry)
            
        self._persist(audit_entry)
        return audit_entry

    def audit_moe_routing(self, routing_stats):
        """Verifica se há especialistas sobrecarregados ou subutilizados."""
        # routing_stats: dict de {expert_id: count}
        total = sum(routing_stats.values())
        imbalance = False
        
        for eid, count in routing_stats.items():
            usage = count / total
            if usage > 0.8: # Um especialista fazendo tudo
                imbalance = True
                self.kernel.log_event("MOE", f"⚖️ Desequilíbrio de Especialistas: Expert {eid} em {usage:.1%}")
        
        if imbalance:
            self.kernel.event_bus.publish("moe_imbalance", routing_stats)

    def _persist(self, entry):
        with open(self.history_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
