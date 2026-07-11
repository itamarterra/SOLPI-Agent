class SOLPISDK:
    """
    PACOTE 2400: SOLPI SDK v1.0
    Ferramentas para desenvolvimento de novos Agentes e Capabilities.
    """
    def __init__(self, brain):
        self.brain = brain

    def register_capability(self, name, agent_class, tags):
        """Permite que plugins registrem novas capacidades em tempo real."""
        self.brain.capability_registry.capabilities[name] = {
            "agent": agent_class,
            "tags": tags
        }
        self.brain.kernel.log_event("SDK", f"Nova capacidade registrada: {name}")
