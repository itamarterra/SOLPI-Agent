import os
import hashlib
import hmac
import re
import ipaddress
import socket
from urllib.parse import urlparse
from pathlib import Path

class SOLPISecurity:
    """
    PACOTE 0002: SECURITY ENGINE v1.0
    Implementa Zero Trust e Secure by Default.
    Responsável por sanitização, hashes e autenticação.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.api_key = os.getenv("SOLPI_API_KEY")

    def validate_path(self, base_dir, requested_path):
        """Impede Directory Traversal."""
        base = Path(base_dir).resolve()
        full = Path(os.path.join(base_dir, requested_path)).resolve()
        try:
            full.relative_to(base)
        except ValueError:
            self.kernel.log_event("SECURITY", f"🚨 TENTATIVA DE TRAVERSAL: {requested_path}")
            raise PermissionError("Acesso ao diretório negado.")
        return str(full)

    def sanitize_input(self, text):
        """Remove caracteres perigosos de comandos e inputs."""
        return re.sub(r'[;&|`$]', '', text)

    def verify_signature(self, message, signature):
        """Valida autenticidade via HMAC-SHA256."""
        if not self.api_key:
            return False
        expected = hmac.new(self.api_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def is_ssrf_safe(self, url):
        """Valida se a URL é segura para requisição externa."""
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False
        if parsed.hostname.lower() == "localhost":
            return False
        try:
            addresses = {item[4][0] for item in socket.getaddrinfo(parsed.hostname, None)}
        except (OSError, ValueError):
            return False
        return bool(addresses) and all(ipaddress.ip_address(address).is_global for address in addresses)
