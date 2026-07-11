import os
import time
import json
from datetime import datetime

class SOLPIWisdomAuditor:
    """
    PACOTE 1900: WISDOM AUDITOR v80.3 (Knowledge Evolution)
    Monitora o crescimento da sabedoria do sistema e envia relatórios de progresso.
    """
    def __init__(self, brain):
        self.brain = brain
        self.kernel = brain.kernel
        self.last_audit_time = 0
        self.wisdom_log_path = "E:/SOLPI-Agent/state/wisdom_growth.json"

    def run_audit(self):
        """Executa a varredura de sabedoria e gera o relatório."""
        self.kernel.log_event("AUDITOR", "Iniciando Auto-Audit de Sabedoria...")
        
        # 1. Contagem de Conhecimento
        total_files = len(self.brain.knowledge.index)
        research_files = sum(1 for f in self.brain.knowledge.index.values() if "RESEARCH" in f["path"])
        skill_files = sum(1 for f in self.brain.knowledge.index.values() if "skills" in f["path"])
        
        # 2. Status do Motor Neural
        engine_status = "OPERACIONAL" if self.brain.neural_vm else "STANDBY"
        active_model = self.brain.config.MODEL_TYPE
        
        # 3. Gera Relatório
        report = (
            f"📈 *SOLPI-OS: RELATÓRIO DE EVOLUÇÃO (v80.3)*\n"
            f"--------------------------------------------\n"
            f"🧠 *CÉREBRO:* {active_model.upper()}\n"
            f"⚙️ *MOTOR:* Neural Engine v80.2\n"
            f"📚 *CONHECIMENTO:* {total_files} arquivos indexados\n"
            f"🔬 *PESQUISA:* {research_files} documentos de elite\n"
            f"🛠️ *HABILIDADES:* {skill_files} ferramentas vivas\n"
            f"📡 *STATUS:* {engine_status}\n"
            f"--------------------------------------------\n"
            f"🚀 *CONCLUSÃO:* A Singularidade cresceu {(total_files * 0.01):.2f}% nesta época."
        )

        # 4. Envia para o WhatsApp do Arquiteto
        self.kernel.log_event("AUDITOR", "Enviando Relatório de Sabedoria via WhatsApp...")
        success = self.brain.tools.send_whatsapp(report)
        
        if success:
            self.kernel.log_event("AUDITOR", "Relatório enviado com sucesso.")
        else:
            self.kernel.log_event("ERROR", "Falha ao enviar relatório via WhatsApp.")

        self.last_audit_time = time.time()
        self._save_wisdom_state(total_files)
        return report

    def _save_wisdom_state(self, count):
        """Persiste o estado da sabedoria para comparação futura."""
        try:
            state = {
                "last_update": str(datetime.now()),
                "knowledge_count": count,
                "version": self.kernel.version
            }
            with open(self.wisdom_log_path, 'w') as f:
                json.dump(state, f, indent=4)
        except: pass
