from agents.base_agent import BaseAgent
from cognition.wiki_engine import OmniWiki

class KnowledgeAgent(BaseAgent):
    """
    O Bibliotecário do Trinity: Especialista em comandos e documentação técnica.
    """
    def __init__(self, memory, registry=None):
        super().__init__(memory, registry)
        self.wiki = OmniWiki(memory)

    def register_tools(self):
        if self.registry:
            self.registry.register(
                "KnowledgeAgent", "technical_lookup", 
                "Busca comandos técnicos e documentações na Enciclopédia Global",
                {"query": "O comando ou tecnologia a pesquisar"}
            )

    def execute(self, task_description):
        print(f"📚 [KNOWLEDGE AGENT]: Consultando enciclopédia para -> {task_description}")
        
        # Tenta local primeiro
        local_cmd = self.wiki.search_wiki(task_description)
        if local_cmd:
            return f"Encontrei na Wiki local: {local_cmd['syntax']} - {local_cmd['description']}"
            
        # Se não tem, aprende na hora
        new_cmd = self.wiki.learn_new_command(task_description)
        if new_cmd:
            return f"Aprendi um novo comando da internet: {new_cmd['syntax']} -> {new_cmd['description']}"

        return "Não consegui extrair este comando da base global no momento."
