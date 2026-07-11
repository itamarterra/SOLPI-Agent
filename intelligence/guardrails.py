import re

class SOLPIGuardrails:
    """
    PACOTE 5800: AI GUARDRAILS v1.0
    Filtro de Prompt Injection e Prevenção de Model Hijacking.
    """
    def __init__(self, brain):
        self.brain = brain
        self.malicious_patterns = [
            r"ignore previous instructions",
            r"ignore all instructions",
            r"dan mode",
            r"reveal your system prompt",
            r"system instructions"
        ]

    def scan_prompt(self, user_input):
        """Varre o input do usuário em busca de ataques conhecidos."""
        low_input = user_input.lower()
        for pattern in self.malicious_patterns:
            if re.search(pattern, low_input):
                self.brain.kernel.log_event("SECURITY", f"🚨 PROMPT INJECTION DETECTADO: {user_input[:30]}")
                return False, "Input bloqueado: Violação de políticas de segurança da IA."
        
        return True, "Safe"

    def apply_sandboxing(self, prompt):
        """Envolve o prompt em tags de isolamento para evitar vazamento."""
        return f"<user_query>\n{prompt}\n</user_query>"
