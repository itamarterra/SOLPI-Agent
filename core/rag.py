import os
import numpy as np

class SOLPIRAG:
    """
    PACOTE 8600: RAG ENGINE v40.0
    Sistema de Recuperação Aumentada por Geração.
    Conecta o Cérebro (LLM) aos documentos técnicos do SOLPI.
    """
    def __init__(self, brain):
        self.brain = brain
        self.research_dir = "E:/SOLPI-RESEARCH"
        self.contexts_last_query = [] # Histórico para o Evaluation Engine

    def retrieve(self, query, top_k=3):
        """Busca os trechos mais relevantes para a pergunta."""
        self.brain.kernel.log_event("RAG", f"Buscando contexto para: {query}")
        
        # 1. Usa o KnowledgeEngine para buscar trechos
        chunks = self.brain.knowledge.get_local_intelligence(query)
        
        if not chunks:
            # Se não achou por palavra-chave simples, tenta o Researcher
            self.brain.kernel.log_event("RAG", "Busca simples falhou. Tentando Researcher...")
            patterns = self.brain.evolution.researcher.scan_for_patterns(query)
            if patterns:
                chunks = [f"💻 Padrão de código encontrado: {p}" for p in patterns]
        
        self.contexts_last_query = chunks
        return chunks[:top_k]

    def augment(self, query, expert_name="Generalist"):
        """Compila o prompt final com o contexto recuperado."""
        context = self.retrieve(query)
        context_str = "\n\n".join(context) if context else "Nenhum contexto adicional encontrado."
        
        # 2. Usa o Prompt Compiler para montar o prompt final para o modelo
        prompt = self.brain.prompt_compiler.compile(
            user_input=query,
            expert_name=expert_name,
            context_data=context_str
        )
        
        return prompt, context_str
