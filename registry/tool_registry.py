import json

class ToolRegistry:
    """
    Catálogo centralizado de capacidades do SOLPI-AIOS.
    Permite que o Reasoner e o Orchestrator saibam exatamente o que o sistema pode fazer.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools = {}
        return cls._instance

    def register(self, agent_name, tool_name, description, parameters=None, permissions="user"):
        """Registra uma ferramenta com metadados detalhados."""
        key = f"{agent_name}.{tool_name}"
        self.tools[key] = {
            "agent": agent_name,
            "name": tool_name,
            "description": description,
            "parameters": parameters or {},
            "permissions": permissions
        }
        print(f"🛠️ [REGISTRY]: Ferramenta '{key}' registrada.")

    def get_tool(self, tool_key):
        return self.tools.get(tool_key)

    def list_all(self):
        return self.tools

    def get_tools_by_agent(self, agent_name):
        return {k: v for k, v in self.tools.items() if v['agent'] == agent_name}
