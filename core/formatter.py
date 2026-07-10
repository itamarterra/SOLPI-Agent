class SOLPIFormatter:
    """
    PACOTE 5000: SEMANTIC FORMATTER v40.0
    Garante que a comunicação do SOLPI seja estruturada, profissional e executiva.
    """
    @staticmethod
    def format_response(expert_name, content, thought_process=None):
        """Formata a resposta final com estrutura Enterprise."""
        header = f"🚀 [SOLPI-OS v40.0] | ESPECIALISTA: {expert_name}"
        divider = "=" * 50
        
        # Constrói o corpo da mensagem
        body = []
        body.append(header)
        body.append(divider)
        
        if thought_process:
            body.append(f"🧠 PENSAMENTO: {thought_process}")
            body.append("-" * 30)
            
        body.append(content)
        
        body.append(divider)
        body.append("⚙️ STATUS: OPERACIONAL | 🛡️ SEGURANÇA: ATIVA")
        
        return "\n".join(body)

    @staticmethod
    def format_infra_report(audit_data, alerts):
        """Formatação específica para relatórios de infraestrutura."""
        res = ["📊 [RELATÓRIO DE OBSERVABILIDADE]"]
        res.append("-" * 40)
        res.append(f"✅ SISTEMA: {'ONLINE' if audit_data else 'OFFLINE'}")
        
        if alerts:
            res.append(f"🚨 ALERTAS ATIVOS: {len(alerts)}")
            for a in alerts:
                res.append(f"  • {a['host']}: {a['trigger']} ({a['severity']})")
        else:
            res.append("🟢 NENHUM ALERTA CRÍTICO DETECTADO.")
            
        res.append("-" * 40)
        res.append("💡 DICA: O sistema de auto-cura está em standby.")
        return "\n".join(res)
