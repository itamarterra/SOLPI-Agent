import json
from cognition.orchestrator import Orchestrator

class SOLPI_MCP_Server:
    """
    Implementação inspirada no mcp-python-sdk da AION-NET.
    Expõe as capacidades do SOLPI OS via Model Context Protocol.
    """
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.protocol_version = "2024-11-05"

    def list_tools(self):
        """Lista todas as ferramentas do Registry no formato MCP."""
        all_tools = self.orchestrator.registry.list_all()
        mcp_tools = []
        for key, info in all_tools.items():
            mcp_tools.append({
                "name": key,
                "description": info["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": info.get("parameters", {})
                }
            })
        return mcp_tools

    def call_tool(self, name, arguments):
        """Executa uma ferramenta via requisição MCP."""
        print(f"🔌 [MCP CALL]: {name} com args {arguments}")
        # O MCP envia para o Orquestrador resolver
        result = self.orchestrator.solve(f"Executar ferramenta {name} com parâmetros {json.dumps(arguments)}")
        return {
            "content": [{"type": "text", "text": str(result)}]
        }

    def list_resources(self):
        """Expõe o GLPI e Zabbix como recursos de dados (padrão AION)."""
        return [
            {"uri": "solpi://glpi/tickets", "name": "Tickets do GLPI"},
            {"uri": "solpi://zabbix/alerts", "name": "Alertas do Zabbix"}
        ]
