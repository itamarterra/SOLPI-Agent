import os
import json

class KnowledgeManager:
    """
    O Bibliotecário do SOLPI-AIOS.
    Gerencia fatos, regras e ferramentas conhecidas.
    """
    def __init__(self, memory):
        self.memory = memory

    def add_fact(self, key, fact, category="general"):
        """Armazena um fato estruturado."""
        content = f"Fact: {key} = {fact}"
        self.memory.store(content, layer="knowledge", tags=category)

    def get_related_facts(self, query):
        """Busca fatos relacionados por similaridade semântica."""
        return self.memory.search(query, layer="knowledge")

    def register_tool_capability(self, tool_name, description):
        """Registra o que uma ferramenta pode fazer na base de conhecimento."""
        self.memory.store(
            f"Tool {tool_name} capability: {description}", 
            layer="knowledge", 
            tags="capability"
        )
