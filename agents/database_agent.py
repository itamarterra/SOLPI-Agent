import pymysql
import os
from agents.base_agent import BaseAgent

class DatabaseAgent(BaseAgent):
    """
    Agente especialista em operações de Banco de Dados.
    """
    def register_tools(self):
        if self.registry:
            self.registry.register(
                "DatabaseAgent", "query", 
                "Executa uma consulta SQL segura",
                {"sql": "String SQL", "params": "Tupla de parâmetros"}
            )

    def execute(self, task_description):
        print(f"🗄️ [DATABASE AGENT]: Executando -> {task_description}")
        
        # Simulação de análise de query via task_description
        if "select" in task_description.lower():
            return self._run_query(task_description)
            
        return "DatabaseAgent: Operação não SQL ignorada."

    def _run_query(self, sql, params=None):
        try:
            conn = pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASS', 'root'),
                database=os.getenv('DB_NAME', 'glpi'),
                cursorclass=pymysql.cursors.DictCursor
            )
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
            conn.close()
            self.log_activity(f"SQL Executada: {sql[:50]}...")
            return result
        except Exception as e:
            return f"Erro DB: {str(e)}"
