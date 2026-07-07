class Reasoner:
    """
    RACIOCÍNIO MULTI-PERSPECTIVA v5.0.
    Simula um debate interno para encontrar a melhor estratégia.
    """
    def __init__(self, memory):
        self.memory = memory

    def ponder(self, objective, context):
        print(f"🤔 [REASONER]: Iniciando debate multi-perspectiva...")
        
        # 1. Analítico (Fatos e Dados)
        analytic = {"view": "Baseado no histórico, este erro de rede é comum no Zabbix.", "conf": 0.92}
        
        # 2. Criativo (Alternativas fora da caixa)
        creative = {"view": "Podemos tentar reiniciar o serviço via SSH em vez de usar a GUI.", "conf": 0.75}
        
        # 3. Crítico (Riscos e Falhas)
        critical = {"view": "Reiniciar o serviço pode causar queda temporária no GLPI.", "conf": 0.95}
        
        # 4. Executor (O 'Como Fazer')
        executor = {"view": "A melhor rota é usar o PowerShellAgent para um restart limpo.", "conf": 0.88}

        debate = [analytic, creative, critical, executor]
        
        # 5. Escolha da melhor síntese
        decision = self._synthesize(debate)
        
        return decision

    def _synthesize(self, perspectives):
        # A confiança média do debate define o Confidence Engine
        avg_conf = sum(p['conf'] for p in perspectives) / len(perspectives)
        return {
            "strategy": perspectives[3]['view'],
            "confidence": round(avg_conf, 2),
            "risk": "Baixo" if avg_conf > 0.8 else "Médio",
            "reasoning_path": [p['view'] for p in perspectives]
        }
