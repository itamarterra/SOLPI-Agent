class SOLPIPolicyEngine:
    """
    PACOTE 8400: POLICY ENGINE v1.0
    Sistema de governança e segurança para ações da IA.
    Define o que o SOLPI-OS pode ou não fazer no PC do Itamar.
    """
    def __init__(self, brain):
        self.brain = brain
        self.rules = {
            "critical_files": [".git", ".env", "kernel.py"],
            "restricted_commands": ["rm -rf", "format", "shutdown"],
            "auto_fix_allowed": True
        }

    def validate_action(self, action_type, target=None):
        """Valida se uma ação está dentro das políticas de segurança."""
        # 1. Checa por comandos proibidos
        if action_type == "COMMAND_EXEC" and target:
            if any(cmd in target.lower() for cmd in self.restricted_commands):
                self.brain.kernel.log_event("POLICY", f"🚨 BLOQUEIO: Comando restrito detectado: {target}")
                return False, "Comando não autorizado pelas políticas de segurança."

        # 2. Checa por proteção de arquivos críticos
        if action_type == "WRITE_FILE" and target:
            if any(f in target for f in self.rules["critical_files"]):
                self.brain.kernel.log_event("POLICY", f"🚨 BLOQUEIO: Tentativa de escrita em arquivo crítico: {target}")
                return False, "Escrita bloqueada para preservar a integridade do Kernel/Config."

        return True, "Ação autorizada."
