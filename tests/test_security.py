import os
import unittest
from unittest.mock import Mock, patch

from execution.tools import AgentTools
from foundation.security import SOLPISecurity


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.kernel = Mock()

    def test_rejects_sibling_path_with_shared_prefix(self):
        security = SOLPISecurity(self.kernel)
        with self.assertRaises(PermissionError):
            security.validate_path(r"E:\SOLPI-Agent\safe", r"..\safe-escape")

    def test_signature_requires_explicit_key(self):
        with patch.dict(os.environ, {}, clear=True):
            security = SOLPISecurity(self.kernel)
            self.assertFalse(security.verify_signature("message", "signature"))

    def test_blocks_private_and_loopback_addresses(self):
        security = SOLPISecurity(self.kernel)
        self.assertFalse(security.is_ssrf_safe("http://127.0.0.1/admin"))
        self.assertFalse(security.is_ssrf_safe("http://172.16.0.1/"))
        self.assertFalse(security.is_ssrf_safe("http://[::1]/"))

    @patch("foundation.security.socket.getaddrinfo")
    def test_rejects_hostname_resolving_to_private_address(self, getaddrinfo):
        getaddrinfo.return_value = [(None, None, None, None, ("10.0.0.8", 0))]
        security = SOLPISecurity(self.kernel)

        self.assertFalse(security.is_ssrf_safe("https://internal.example"))


class DatabaseConfigurationTests(unittest.TestCase):
    @patch("execution.tools.pymysql.connect")
    @patch.dict(
        os.environ,
        {"DB_HOST": "db.example", "DB_PORT": "3307", "DB_USER": "agent", "DB_PASS": "secret", "DB_NAME": "solpi"},
        clear=False,
    )
    def test_connection_uses_environment_configuration(self, connect):
        AgentTools._db_connection()

        connect.assert_called_once_with(
            host="db.example",
            port=3307,
            user="agent",
            password="secret",
            database="solpi",
            connect_timeout=1,
        )


if __name__ == "__main__":
    unittest.main()
