from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

class SOLPIGatewayHandler(BaseHTTPRequestHandler):
    """Handler oficial do SOLPI-OS para requisições externas."""
    
    def do_GET(self):
        """Endpoints de Observabilidade Visual."""
        if self.path == "/twin":
            self._serve_html_dashboard()
        elif self.path == "/api/twin_data":
            self._serve_json_metrics()
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        """Endpoints de Comando e Webhooks (WhatsApp/GLPI)."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request = json.loads(post_data)
        
        # 1. Webhook Evolution API
        if request.get("event") == "messages.upsert":
            self._handle_whatsapp(request)
            res = {"status": "ACK"}
        # 2. Comando Direto para o Brain
        else:
            response_text = SOLPIGateway.brain.process(request.get("command", ""))
            res = {"status": "success", "response": response_text}
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())

    def _serve_json_metrics(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Coleta dados do Domínio de Operações
        stats = SOLPIGateway.brain.telemetry.get_snapshot()
        twin_data = SOLPIGateway.brain.twin.get_state()
        self.wfile.write(json.dumps(twin_data).encode())

    def _handle_whatsapp(self, request):
        """Trata interações de botões via Barramento de Serviços."""
        msg = request.get("data", {}).get("message", {})
        if "buttonsResponseMessage" in msg:
            btn_id = msg["buttonsResponseMessage"]["selectedButtonId"]
            SOLPIGateway.brain.kernel.service_bus.publish("WHATSAPP", "BUTTON_CLICK", {"id": btn_id})

    def _serve_html_dashboard(self):
        """Serve a interface 3D do Digital Twin."""
        self.send_response(200); self.send_header('Content-type', 'text/html'); self.end_headers()
        # ... (HTML do Dashboard Three.js movido para ca)
        self.wfile.write(b"<h1>SOLPI-OS Digital Twin v50.5</h1>")

class SOLPIGateway:
    """
    PACOTE 2200: DEVELOPER GATEWAY v50.5
    Porta de entrada externa do SOLPI-OS.
    """
    brain = None

    def __init__(self, brain, port=8090):
        SOLPIGateway.brain = brain
        self.port = port
        try:
            self.server = HTTPServer(('0.0.0.0', port), SOLPIGatewayHandler)
        except: self.server = None

    def start(self):
        if self.server:
            print(f"🌐 [DEVELOPER]: API Gateway Ativo em http://0.0.0.0:{self.port}")
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
