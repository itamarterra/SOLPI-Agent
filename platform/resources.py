class SOLPIResourceManager:
    """
    PACOTE 9700: AI RESOURCE MARKET v1.0
    Controla a "Economia de Tokens" e Orçamentos de Hardware.
    Garante que nenhum agente esgote os recursos do Itamar.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.budgets = {
            "GLOBAL_TOKENS": 1000000,
            "MAX_GPU_LOAD": 0.8,
            "MAX_RAM_GB": 8.0
        }
        self.consumption = {"tokens": 0, "compute": 0}

    def allocate_tokens(self, amount, agent_name):
        """Negocia o uso de tokens para uma tarefa."""
        if self.consumption["tokens"] + amount > self.budgets["GLOBAL_TOKENS"]:
            self.kernel.log_event("RESOURCES", f"🚨 ORÇAMENTO ESGOTADO: {agent_name} solicitou {amount} tokens.")
            return False
            
        self.consumption["tokens"] += amount
        self.kernel.log_event("RESOURCES", f"💰 {agent_name} consumiu {amount} tokens. (Total: {self.consumption['tokens']})")
        return True

    def get_market_status(self):
        return {
            "token_usage": f"{(self.consumption['tokens'] / self.budgets['GLOBAL_TOKENS']) * 100:.2f}%",
            "compute_health": "OPTIMAL"
        }
