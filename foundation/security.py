import os
import hashlib
import hmac
import re
from pathlib import Path

class SOLPISecurity:
    """
    PACOTE 0002: SECURITY ENGINE v1.0
    Implementa Zero Trust e Secure by Default.
    Responsável por sanitização, hashes e autenticação.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.api_key = os.getenv("SOLPI_API_KEY", "PROTECTED_DEFAULT")

    def validate_path(self, base_dir, requested_path):
        """Impede Directory Traversal."""
        base = Path(base_dir).resolve()
        full = Path(os.path.join(base_dir, requested_path)).resolve()
        if not str(full).startswith(str(base)):
            self.kernel.log_event("SECURITY", f"🚨 TENTATIVA DE TRAVERSAL: {requested_path}")
            raise PermissionError("Acesso ao diretório negado.")
        return str(full)

    def sanitize_input(self, text):
        """Remove caracteres perigosos de comandos e inputs."""
        return re.sub(r'[;&|`$]', '', text)

    def verify_signature(self, message, signature):
        """Valida autenticidade via HMAC-SHA256."""
        expected = hmac.new(self.api_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def is_ssrf_safe(self, url):
        """Valida se a URL é segura para requisição externa."""
        forbidden_patterns = [r"localhost", r"127\.0\.0\.1", r"192\.168\.", r"10\."]
        for pattern in forbidden_patterns:
            if re.search(pattern, url):
                return False
        return url.startswith(("http://", "https://"))
