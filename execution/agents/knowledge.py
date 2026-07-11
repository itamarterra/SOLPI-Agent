from execution.agents.base import BaseAgent

class KnowledgeAgent(BaseAgent):
    """
    PACOTE 1603: KNOWLEDGE AGENT v50.0
    Bibliotecário cognitivo e interface RAG.
    """
    def run(self, query):
        local = self.brain.knowledge.get_local_intelligence(query)
        if local:
            return "📚 **CONHECIMENTO ENCONTRADO:**\n" + "\n".join(local)
        return "🔍 Nenhuma base local. Pesquisando em bibliotecas de elite no Drive E:..."
