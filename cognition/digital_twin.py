import json
from datetime import datetime

class DigitalTwin:
    """
    O Gêmeo Digital do SOLPI OS v5.3.
    Mantém um modelo virtual da infraestrutura física e lógica (Servidores, Redes, Containers).
    Permite simular o impacto de mudanças antes da execução real.
    """
    def __init__(self, memory):
        self.memory = memory
        self.model = {
            "infrastructure": {},
            "topology": [],
            "last_sync": None
        }

    def sync_from_sources(self, zabbix_data=None, glpi_data=None):
        """Atualiza o modelo virtual com dados reais das integrações."""
        print("🖇️ [DIGITAL TWIN]: Sincronizando modelo com Zabbix e GLPI...")
        
        # Simulação de mapeamento de infraestrutura
        if zabbix_data:
            for host in zabbix_data:
                self.model["infrastructure"][host['name']] = {
                    "type": "server",
                    "status": host['status'],
                    "metrics": host.get('metrics', {})
                }
        
        self.model["last_sync"] = datetime.now().isoformat()
        self.memory.store(json.dumps(self.model), layer="knowledge", tags="digital_twin_state")
        return self.model

    def predict_impact(self, action, target_node):
        """Simula o impacto de uma ação em um nó específico da infraestrutura."""
        print(f"🔮 [DIGITAL TWIN]: Simulando impacto de '{action}' em '{target_node}'...")
        
        node = self.model["infrastructure"].get(target_node)
        if not node:
            return {"risk": "Desconhecido", "impact": "Nó não mapeado no Gêmeo Digital."}

        # Exemplo de lógica preditiva
        if action == "restart" and node["status"] == "critical":
            return {"risk": "Baixo", "impact": "Recuperação de serviço necessária."}
        
        return {"risk": "Médio", "impact": "Possível indisponibilidade temporária de dependentes."}

    def get_topology(self):
        return self.model["topology"]
