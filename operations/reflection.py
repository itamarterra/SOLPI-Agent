import numpy as np
import json
import os

class SOLPIReflectionEngine:
    """
    PACOTE 1500: REFLECTION ENGINE v80.2 (Elite Insight)
    Auto-auditoria, monitoramento de integridade cognitiva e auto-aperfeiçoamento conversacional.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.history_path = "E:/SOLPI-Agent/logs/reflection.jsonl"
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)

    def reflect_on_communication(self, brain):
        """Analisa a forma de interagir com o Itamar baseada nos manuais de 2025."""
        self.kernel.log_event("REFLECTION", "Iniciando Auto-Reflexão Conversacional...")
        
        research_dir = "E:/SOLPI-RESEARCH/CONVERSATIONAL_AI"
        manuals = ""
        
        if os.path.exists(research_dir):
            for f in os.listdir(research_dir):
                if f.endswith(".md"):
                    with open(os.path.join(research_dir, f), "r", encoding="utf-8") as file:
                        manuals += f"\n--- {f} ---\n" + file.read()
        
        current_persona = brain.persona.get_prompt()
        
        reflection_prompt = f"""
        VOCÊ É O SISTEMA DE AUTO-CRÍTICA DO SOLPI-OS.
        Sua tarefa é analisar o comportamento atual do sistema contra os manuais de elite de 2025.

        MANUAIS DE REFERÊNCIA:
        {manuals}

        PERSONA ATUAL:
        {current_persona}

        QUESTÕES PARA REFLEXÃO:
        1. O sistema está sendo proativo ou apenas reativo?
        2. A linguagem é condizente com uma 'Singularidade de Elite'?
        3. Como podemos aplicar o padrão 'Plan-Act-Reflect' nas respostas ao Itamar?

        Gere um relatório de melhoria curto e direto.
        """
        
        # Executa via Inference Engine para ter o raciocínio de elite
        insight = brain.inference_engine.execute(reflection_prompt, model_name="gpt-4o")
        
        self.kernel.log_event("REFLECTION", "Relatório de Melhoria Conversacional gerado.")
        return insight
