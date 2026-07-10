from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

class SOLPIGatewayHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request = json.loads(post_data)
        
        # Orquestra o pedido via Brain
        response_text = SOLPIGateway.brain.process(request.get("command", ""))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "response": response_text}).encode())

class SOLPIGateway:
    """
    PACOTE 2201: API GATEWAY v1.0
    Servidor HTTP para integração com GLPI e sistemas externos.
    """
    brain = None # Estático para o Handler

    def __init__(self, brain, port=8090):
        SOLPIGateway.brain = brain
        self.port = port
        self.server = HTTPServer(('localhost', port), SOLPIGatewayHandler)

    def start(self):
        print(f"🌐 [GATEWAY]: SOLPI-OS API ativa na porta {self.port}")
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
