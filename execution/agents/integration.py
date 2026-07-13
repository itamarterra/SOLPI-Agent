from execution.agents.base import BaseAgent


class IntegrationAgent(BaseAgent):
    """Expõe as operações do plugin SOLPI/GLPI ao orquestrador."""

    def run(self, context=None):
        query = (context or "").lower()
        worker_terms = ("worker", "fila", "processar", "processamento", "integração", "integracao")

        if any(term in query for term in worker_terms):
            return self.brain.tools.run_integration_worker()

        return self.brain.tools.get_dashboard_metrics()
