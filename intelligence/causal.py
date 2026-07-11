class SOLPICausalEngine:
    """
    PACOTE 5300: CAUSAL ENGINE v50.8
    O "Motor de Porquês". Entende relações de Causa e Efeito.
    Transforma correlações em conhecimento causal para diagnóstico de ITSM.
    """
    def __init__(self, brain):
        self.brain = brain
        self.causal_graph = {} # { "efeito": { "causa": probabilidade } }

    def register_event(self, cause, effect, success=True):
        """Registra um link causal baseado no resultado de uma ação."""
        if effect not in self.causal_graph:
            self.causal_graph[effect] = {}
            
        if cause not in self.causal_graph[effect]:
            self.causal_graph[effect][cause] = 0.5 # Probabilidade inicial
            
        # Reforço positivo ou negativo
        if success:
            self.causal_graph[effect][cause] = min(1.0, self.causal_graph[effect][cause] + 0.1)
        else:
            self.causal_graph[effect][cause] = max(0.0, self.causal_graph[effect][cause] - 0.1)
            
        self.brain.kernel.log_event("CAUSAL", f"Link atualizado: {cause} -> {effect} (Prob: {self.causal_graph[effect][cause]:.2f})")

    def infer_cause(self, effect):
        """Tenta identificar a causa mais provável para um problema."""
        if effect in self.causal_graph:
            causes = self.causal_graph[effect]
            best_cause = max(causes, key=causes.get)
            return best_cause, causes[best_cause]
        return None, 0.0

    def explain_relationship(self, cause, effect):
        """Gera uma explicação humana sobre a relação causal."""
        prob = self.causal_graph.get(effect, {}).get(cause, 0.0)
        if prob > 0.8:
            return f"A ação '{cause}' tem alta probabilidade de resolver o problema '{effect}'."
        return f"Não há evidências causais fortes entre '{cause}' e '{effect}' ainda."
