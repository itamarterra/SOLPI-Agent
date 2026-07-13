import unittest
import os
from unittest.mock import Mock, patch

from execution.agents.integration import IntegrationAgent
from execution.registry import SOLPICapabilityRegistry
from execution.tools import AgentTools


class GlpiApiTests(unittest.TestCase):
    @patch("execution.tools.requests.post")
    def test_accepts_created_response(self, post):
        response = Mock(status_code=201, content=b'{"processed": 3}')
        response.json.return_value = {"processed": 3}
        post.return_value = response

        self.assertEqual(
            AgentTools.glpi_api("POST", "integration-engine/worker/run-once", {"limit": 20}),
            {"processed": 3},
        )
        self.assertTrue(post.call_args.args[0].endswith("/integration-engine/worker/run-once"))

    @patch("execution.tools.requests.get")
    def test_accepts_empty_success_response(self, get):
        get.return_value = Mock(status_code=204, content=b"")
        self.assertEqual(AgentTools.glpi_api("GET", "/dashboard"), {})

    @patch("execution.tools.requests.get")
    def test_unwraps_solpi_api_response(self, get):
        response = Mock(status_code=200, content=b'{"status":"ok","data":{"open_tickets":4}}')
        response.json.return_value = {"status": "ok", "data": {"open_tickets": 4}}
        get.return_value = response

        self.assertEqual(AgentTools.glpi_api("GET", "/dashboard"), {"open_tickets": 4})

    @patch.dict(os.environ, {"SOLPI_GLPI_API_KEY": "test-key"}, clear=False)
    @patch("execution.tools.requests.get")
    def test_uses_public_api_url_and_authentication_header(self, get):
        get.return_value = Mock(status_code=204, content=b"")

        AgentTools.glpi_api("GET", "/health")

        self.assertEqual(get.call_args.args[0], "http://localhost:8081/plugins/solpi/api/index.php/health")
        self.assertEqual(get.call_args.kwargs["headers"]["X-API-Key"], "test-key")

    def test_rejects_invalid_worker_limit(self):
        self.assertIn("entre 1 e 100", AgentTools.run_integration_worker(0))


class IntegrationAgentTests(unittest.TestCase):
    def test_routes_worker_request_to_worker_tool(self):
        tools = Mock()
        tools.run_integration_worker.return_value = "worker ran"
        agent = IntegrationAgent(Mock(tools=tools))

        self.assertEqual(agent.run("processe a fila de integração"), "worker ran")
        tools.run_integration_worker.assert_called_once_with()

    def test_routes_dashboard_request_to_metrics_tool(self):
        tools = Mock()
        tools.get_dashboard_metrics.return_value = "metrics"
        agent = IntegrationAgent(Mock(tools=tools))

        self.assertEqual(agent.run("mostre o dashboard"), "metrics")
        tools.get_dashboard_metrics.assert_called_once_with()


class IntegrationRoutingTests(unittest.TestCase):
    def test_dashboard_glpi_has_priority_over_sql_routing(self):
        brain = Mock()
        brain.solpi_engine_agent.get_available_tools.return_value = []
        registry = SOLPICapabilityRegistry(brain)

        self.assertEqual(registry.resolve("mostre o dashboard do GLPI"), "INTEGRATION_AGENT")


if __name__ == "__main__":
    unittest.main()
