from execution.agents.base import BaseAgent

class InfraAgent(BaseAgent):
    """
    PACOTE 1600: INFRA AGENT v50.0
    Especialista em Observabilidade, Zabbix e Auto-Cura de Containers.
    """
    def run(self, context=None):
        self.kernel.log_event("INFRA", "Varredura de infraestrutura iniciada.")
        
        # Snapshot do Sistema
        audit = self.brain.tools.self_audit()
        
        # Monitoramento Zabbix
        alerts = self.brain.tools.get_zabbix_alerts()
        critical = [a for a in alerts if a['severity'] == "Desastre"]
        
        report = []
        report.append(f"**SNAPSHOT:** {' | '.join(audit[:2])}")
        
        if critical:
            report.append("\n🚨 **INCIDENTES CRÍTICOS:**")
            for a in critical:
                msg = f"{a['host']}: {a['trigger']}"
                report.append(f"  • {msg}")
                # Automação de Ticket
                self.brain.tools.create_glpi_ticket(f"ALERTA: {a['trigger']}", msg)
        else:
            report.append("🟢 Nenhuma anomalia crítica detectada.")
            
        return "\n".join(report)
