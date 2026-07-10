from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

class SOLPIGatewayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve o Dashboard 3D do Digital Twin (v40.0)"""
        if self.path == "/twin":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Dashboard Minimalista 3D
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>SOLPI-OS Digital Twin 3D</title>
                <script src="https://unpkg.com/3d-force-graph"></script>
                <style> body { margin: 0; background: #000; color: #0f0; font-family: monospace; } </style>
            </head>
            <body>
                <div id="3d-graph"></div>
                <div style="position: absolute; top: 10px; left: 10px; z-index: 10;">
                    <h1>SOLPI-OS DIGITAL TWIN v40.0</h1>
                    <div id="metrics">Sincronizando...</div>
                </div>
                <script>
                    const Graph = ForceGraph3D()(document.getElementById('3d-graph'))
                        .jsonUrl('/api/twin_data')
                        .nodeAutoColorBy('group')
                        .nodeLabel(node => `${node.id}: ${node.status || 'Active'}`);
                    
                    // Update loop
                    setInterval(() => {
                        fetch('/api/twin_data').then(r => r.json()).then(data => {
                            document.getElementById('metrics').innerText = 
                                `CPU: ${data.metrics.cpu} | RAM: ${data.metrics.ram} | TOKENS: ${data.metrics.tokens}`;
                        });
                    }, 5000);
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        elif self.path == "/api/twin_data":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Formata dados para o 3D-Force-Graph
            stats = SOLPIGateway.brain.telemetry.get_stats()
            twin_state = SOLPIGateway.brain.twin.sync()
            
            payload = {
                "nodes": [
                    {"id": "Kernel", "group": 1},
                    {"id": "NeuralCore", "group": 2},
                    {"id": "MoE_Router", "group": 2},
                    {"id": "Expert_0", "group": 3},
                    {"id": "Expert_1", "group": 3},
                    {"id": "Expert_2", "group": 3},
                    {"id": "Expert_3", "group": 3},
                    {"id": "Zabbix_Link", "group": 4},
                    {"id": "WhatsApp_GW", "group": 4}
                ],
                "links": [
                    {"source": "Kernel", "target": "NeuralCore"},
                    {"source": "NeuralCore", "target": "MoE_Router"},
                    {"source": "MoE_Router", "target": "Expert_0"},
                    {"source": "MoE_Router", "target": "Expert_1"},
                    {"source": "MoE_Router", "target": "Expert_2"},
                    {"source": "MoE_Router", "target": "Expert_3"},
                    {"source": "Kernel", "target": "Zabbix_Link"},
                    {"source": "Kernel", "target": "WhatsApp_GW"}
                ],
                "metrics": {
                    "cpu": stats.get("cpu_usage"),
                    "ram": stats.get("ram_usage"),
                    "tokens": stats.get("total_tokens")
                }
            }
            self.wfile.write(json.dumps(payload).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request = json.loads(post_data)
        
        # 1. Detectar se é um Webhook da Evolution API (Botões)
        if request.get("event") == "messages.upsert":
            self.handle_whatsapp_event(request)
            response_data = {"status": "event_received"}
        else:
            # 2. Orquestra o pedido via Brain (Comando Direto)
            response_text = SOLPIGateway.brain.process(request.get("command", ""))
            response_data = {"status": "success", "response": response_text}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def handle_whatsapp_event(self, request):
        """Processa interações de botões do WhatsApp."""
        try:
            msg = request.get("data", {}).get("message", {})
            if "buttonsResponseMessage" in msg:
                btn_id = msg["buttonsResponseMessage"]["selectedButtonId"]
                SOLPIGateway.brain.kernel.log_event("WHATSAPP", f"Botão pressionado: {btn_id}")
                
                if btn_id.startswith("approve_"):
                    action_id = btn_id.replace("approve_", "")
                    SOLPIGateway.brain.event_bus.publish("action_approved", {"id": action_id})
                elif btn_id.startswith("reject_"):
                    action_id = btn_id.replace("reject_", "")
                    SOLPIGateway.brain.event_bus.publish("action_rejected", {"id": action_id})
        except Exception as e:
            print(f"❌ Erro no Webhook WhatsApp: {e}")

class SOLPIGateway:
    """
    PACOTE 2201: API GATEWAY v1.0
    Servidor HTTP para integração com GLPI e sistemas externos.
    """
    brain = None # Estático para o Handler

    def __init__(self, brain, port=8090):
        SOLPIGateway.brain = brain
        self.port = port
        try:
            self.server = HTTPServer(('0.0.0.0', port), SOLPIGatewayHandler)
        except Exception as e:
            print(f"❌ [GATEWAY ERROR]: Não foi possível iniciar na porta {port}: {e}")
            self.server = None

    def start(self):
        if self.server:
            print(f"🌐 [GATEWAY]: SOLPI-OS API ativa em http://0.0.0.0:{self.port}")
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
        else:
            print("⚠️ [GATEWAY]: Servidor não inicializado. Verifique se a porta 8090 está livre.")
