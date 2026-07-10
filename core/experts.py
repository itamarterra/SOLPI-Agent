class BaseExpert:
    def __init__(self, brain):
        self.brain = brain

class InfraExpert(BaseExpert):
    """Especialista em Redes, Docker e Zabbix."""
    def run(self):
        audit = self.brain.tools.self_audit()
        return "📡 [INFRA-REPORT]: Sistema analisado. Conclusão: " + " | ".join(audit)

class DevExpert(BaseExpert):
    """Especialista em Python, PHP e Correção de Código."""
    def run(self, task):
        # Usa o researcher para buscar padrões no disco E:
        examples = self.brain.researcher.scan_for_patterns(task)
        return f"💻 [DEV-REPORT]: Analisando lógica para '{task}'. Referências encontradas: {len(examples)}."

class KnowledgeExpert(BaseExpert):
    """Especialista em RAG e Documentação Corporativa."""
    def run(self, query):
        local = self.brain.knowledge.get_local_intelligence(query)
        return "📚 [KNOWLEDGE-REPORT]: " + ("\n".join(local) or "Nenhuma base local encontrada. Sugiro baixar o site oficial.")
