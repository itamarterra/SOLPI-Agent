class SOLPIFormatter:
    """
    PACOTE 5000: SEMANTIC FORMATTER v40.1
    Garante que a comunicação do SOLPI seja natural e parceira (Estilo Humano).
    Foco total em uma interface limpa e conversacional.
    """
    @staticmethod
    def format_response(expert_name, content, thought_process=None):
        """Formata a resposta para parecer um diálogo de consultoria ou chat direto."""
        
        # Se for GENERALIST ou Chat, retornamos APENAS a resposta (Estilo ChatGPT)
        if expert_name in ["GENERALIST", "ORQUESTRADOR", "SOLPI_ENGINE_AGENT"]:
            return f"🤖 **SOLPI:** {content}"

        # Para agentes técnicos (INFRA, DEV, SQL), mantemos um SNAPSHOT estruturado
        res = []
        res.append(f"🤖 **SOLPI** [{expert_name}]:")
        res.append("-" * 30)
        
        if thought_process:
            res.append(f"💡 *{thought_process}*")
            res.append("")
            
        res.append(content)
        res.append("-" * 30)
        
        return "\n".join(res)

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
        return "\n".join(res)
