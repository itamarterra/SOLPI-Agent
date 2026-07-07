import requests
import os
from agents.base_agent import BaseAgent

class ZabbixAgent(BaseAgent):
    """
    Agente especialista em monitoramento Zabbix.
    """
    def register_tools(self):
        self.registry.register("ZabbixAgent", "get_alerts", "Recupera alertas ativos do Zabbix")
        self.registry.register("ZabbixAgent", "ack_event", "Reconhece um evento no Zabbix")

    def execute(self, task_description):
        print(f"📡 [ZABBIX AGENT]: Consultando -> {task_description}")
        
        if "alertas" in task_description.lower() or "status" in task_description.lower():
            return self._fetch_alerts()
            
        return "ZabbixAgent: Tarefa concluída."

    def _fetch_alerts(self):
        # Simulação de chamada API Zabbix
        self.log_activity("Consultou alertas no Zabbix")
        return "Zabbix: 2 problemas ativos (CPU High, Disk Full)."
