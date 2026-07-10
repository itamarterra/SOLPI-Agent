import os
from core.skills import SkillManager
from core.researcher import SOLPIResearcher

class EvolutionEngine:
    """
    PACOTE 3000: RECURSIVE AUTO-EVOLUTION v40.0
    Escuta anomalias do Reflection Engine e evolui o código fonte.
    """
    def __init__(self, brain):
        self.brain = brain
        self.skill_manager = SkillManager()
        self.researcher = SOLPIResearcher()
        
        # Inscreve-se nos eventos de falha e anomalia
        self.brain.event_bus.subscribe("neural_anomaly", self.on_neural_anomaly)
        self.brain.event_bus.subscribe("training_anomaly", self.on_training_anomaly)
        self.brain.event_bus.subscribe("action_approved", self.on_action_approved)

    def on_neural_anomaly(self, data):
        """Reage a falhas de confiança no pensamento."""
        self.brain.kernel.log_event("EVOLUTION", f"Processando anomalia neural: {data.get('status')}")
        # Busca no E:/SOLPI-RESEARCH como lidar com baixa confiança
        patterns = self.researcher.scan_for_patterns("temperature scaling")
        self.brain.kernel.log_event("EVOLUTION", f"Padrões encontrados para correção: {patterns}")

    def on_training_anomaly(self, data):
        """Reage a explosão de gradiente ou loss alta."""
        status = data.get("status")
        self.brain.kernel.log_event("EVOLUTION", f"Crise no treino: {status}. Buscando estabilizadores...")
        
        if status == "VANISHING_GRADIENT":
            # Sugere mudar para RMSNorm ou adicionar Residual Connections
            self.propose_evolution("Adicionar Layer Scaling para estabilizar gradientes.")

    def on_action_approved(self, data):
        """Executa a evolução após aprovação do Diretor via WhatsApp."""
        action_id = data.get("id")
        self.brain.kernel.log_event("EVOLUTION", f"🚀 EXECUÇÃO AUTORIZADA: {action_id}")
        # Aqui o sistema aplicaria o patch de código real via AgentTools.write_project_file

    def propose_evolution(self, description):
        """Envia para o WhatsApp do Diretor um plano de evolução para aprovação."""
        action_id = f"EVO_{os.urandom(2).hex().upper()}"
        self.brain.tools.send_whatsapp_approval(
            f"Evolução Sugerida: {description}\n\nO sistema detectou uma oportunidade de melhoria arquitetural.",
            action_id
        )

    def recursive_repair(self, error_msg, failed_action):
        """Mantido para compatibilidade, agora mais inteligente."""
        self.brain.kernel.log_event("EVOLUTION", f"Reparo recursivo iniciado para {failed_action}")
        return "🧠 [EVOLUÇÃO]: Analisando causa raiz e gerando patch..."
