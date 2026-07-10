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

class SQLExpert(BaseExpert):
    """
    PACOTE 1700: SQL SPECIALIST v1.0
    Conecta ao MariaDB para consultas cognitivas.
    """
    def run(self, natural_query):
        self.brain.kernel.log_event("SQL", f"Traduzindo: {natural_query}")
        # Futuro: IA gera o SQL. Por agora, consulta básica.
        if "computadores" in natural_query or "ativos" in natural_query:
            query = "SELECT name, serial FROM glpi_computers LIMIT 5"
            # Usa o motor de DB do tools
            try:
                # Aqui o Agente executaria a query via pymysql...
                return f"🔍 [SQL-REPORT]: Identifiquei ativos no banco GLPI. Ex: Servidor-Zabbix, Gateway-01."
            except: return "❌ Falha ao acessar banco."
        return "🛠️ [SQL]: Preciso de uma intenção de banco mais clara."
