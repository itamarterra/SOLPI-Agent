import pymysql
from execution.agents.base import BaseAgent

class SQLAgent(BaseAgent):
    """
    PACOTE 1700: SQL AGENT v50.0
    Engenheiro de Dados especializado no esquema GLPI.
    """
    def run(self, natural_query):
        cmd = natural_query.lower()
        self.kernel.log_event("SQL", f"Query Cognitiva: {natural_query}")
        
        # Mapeamento Rápido
        if any(x in cmd for x in ["computador", "ativo"]):
            return self._exec("SELECT name, serial FROM glpi_computers LIMIT 5", "Ativos")
        if any(x in cmd for x in ["chamado", "ticket"]):
            return self._exec("SELECT id, name FROM glpi_tickets WHERE status=1 LIMIT 5", "Tickets")
            
        return "🛠️ [SQL]: Intenção de banco não mapeada."

    def _exec(self, sql, label):
        try:
            conn = pymysql.connect(host='localhost', port=3306, user='glpi', password='glpi', database='glpi')
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
            conn.close()
            return f"📊 **{label}**: \n" + "\n".join([f"- {' | '.join(map(str, r))}" for r in rows])
        except Exception as e:
            return f"❌ Erro SQL: {e}"
