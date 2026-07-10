import time
import numpy as np

class SOLPIPredictor:
    """
    PACOTE 7000: PREDICTIVE ENGINE v40.0
    Analisa tendências de telemetria para prever falhas de infraestrutura.
    """
    def __init__(self, brain):
        self.brain = brain

    def analyze_trends(self):
        """Calcula velocidade de consumo de recursos."""
        history = self.brain.telemetry.history
        if len(history) < 2: return None
        
        # 1. Análise de Disco
        first, last = history[0], history[-1]
        time_diff = (last['t'] - first['t']) / 3600 # horas
        disk_diff = first['disk_free'] - last['disk_free'] # GB consumidos
        
        if time_diff > 0 and disk_diff > 0:
            burn_rate = disk_diff / time_diff # GB por hora
            time_to_empty = last['disk_free'] / burn_rate
            
            if time_to_empty < 24: # Alerta se faltar menos de um dia
                return {
                    "type": "DISK_CRITICAL",
                    "burn_rate": burn_rate,
                    "eta_hours": time_to_empty,
                    "message": f"Previsão: Disco ficará cheio em {time_to_empty:.1f} horas (Consumo: {burn_rate:.2f}GB/h)"
                }
        
        return None

    def check_and_alert(self):
        prediction = self.analyze_trends()
        if prediction:
            self.brain.kernel.log_event("PREDICTOR", f"🚨 ALERTA PREDITIVO: {prediction['message']}")
            # Notifica o Diretor via WhatsApp
            self.brain.tools.send_whatsapp(f"🔮 *PREVISÃO DE FALHA*\n\n{prediction['message']}\n\nDeseja que eu execute limpeza preventiva?")
            return prediction
        return None
