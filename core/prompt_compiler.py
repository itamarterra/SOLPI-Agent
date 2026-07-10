import json

class SOLPIPromptCompiler:
    """
    PACOTE 8300: PROMPT COMPILER v1.0
    Transforma intenções e dados em prompts otimizados para o modelo.
    Gerencia Contexto, Políticas, Histórico e Memória de forma unificada.
    """
    def __init__(self, brain):
        self.brain = brain
        self.templates = {
            "default": "Usuário: {input}\nContexto: {context}\nResposta: ",
            "expert": "Você é o {expert_name}.\nHistórico: {history}\nConhecimento: {knowledge}\nTarefa: {input}\nResposta Técnica: "
        }

    def compile(self, user_input, expert_name="Generalist", context_data=None):
        """Monta o prompt final (Etapa 8302)."""
        # 1. Coleta Histórico da Memória
        history = self.brain.memory.short_term[-3:]
        history_str = " | ".join([f"{h['r']}: {h['c']}" for h in history])
        
        # 2. Coleta Conhecimento (RAG)
        knowledge = self.brain.knowledge.get_local_intelligence(user_input)
        knowledge_str = "\n".join(knowledge[:2])
        
        # 3. Aplica Políticas (Policy Engine Placeholder)
        policy_check = "Ação autorizada por padrão (ADMIN)."
        
        # 4. Seleciona Template
        template = self.templates.get("expert")
        
        # 5. Compilação Final
        prompt = template.format(
            expert_name=expert_name,
            history=history_str,
            knowledge=knowledge_str,
            input=user_input
        )
        
        self.brain.kernel.log_event("COMPILER", f"Prompt compilado para {expert_name}")
        return prompt
