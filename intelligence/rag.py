import os
import numpy as np

class SOLPIRAG:
    """
    PACOTE 8600: RAG ENGINE v50.0
    Recuperação Aumentada agora integrada ao domínio de Intelligence.
    """
    def __init__(self, brain):
        self.brain = brain
        self.research_dir = "E:/SOLPI-RESEARCH"
        self.contexts_last_query = []

    def retrieve(self, query, top_k=3):
        self.brain.kernel.log_event("RAG", f"Buscando no Drive E: {query}")
        chunks = self.brain.knowledge.get_local_intelligence(query)
        
        if not chunks:
            patterns = self.brain.evolution.researcher.scan_for_patterns(query)
            if patterns:
                chunks = [f"💻 Padrão: {p}" for p in patterns]
        
        self.contexts_last_query = chunks
        return chunks[:top_k]

    def augment(self, query, expert_name="Generalist"):
        context = self.retrieve(query)
        context_str = "\n\n".join(context) if context else ""
        prompt = self.brain.prompt_compiler.compile(query, expert_name, context_str)
        return prompt, context_str
