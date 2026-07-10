class SOLPIFormatter:
    """
    PACOTE 5000: SEMANTIC FORMATTER v40.0
    Garante que a comunicação do SOLPI seja natural e parceira (Estilo Humano).
    """
    @staticmethod
    def format_response(expert_name, content, thought_process=None):
        """Formata a resposta para parecer um diálogo de consultoria."""
        # Se for uma resposta genérica ou de orquestrador, remove o header pesado
        if expert_name == "ORQUESTRADOR":
            return content

        res = []
        res.append(f"🤖 **SOLPI** ({expert_name}):")
        res.append("-" * 20)
        
        if thought_process:
            res.append(f"*Analisei seu pedido e {thought_process.lower()}*")
            res.append("")
            
        res.append(content)
        res.append("-" * 20)
        res.append("O que você achou dessa solução? Podemos avançar para o próximo passo?")
        
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
        res.append("💡 DICA: O sistema de auto-cura está em standby.")
        return "\n".join(res)
