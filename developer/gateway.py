from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import os

class SOLPIGatewayHandler(BaseHTTPRequestHandler):
    """Handler oficial do SOLPI-OS para requisições externas."""
    
    def do_GET(self):
        """Endpoints de Observabilidade Visual."""
        if self.path == "/" or self.path == "/twin":
            self._serve_html_dashboard()
        elif self.path == "/api/twin_data":
            self._serve_json_metrics()
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        """Endpoints de Comando e Webhooks."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request = json.loads(post_data)
        
        response_text = SOLPIGateway.brain.process(request.get("command", ""))
        res = {"status": "success", "response": response_text}
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())

    def _serve_json_metrics(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        twin_data = SOLPIGateway.brain.twin.get_state()
        self.wfile.write(json.dumps(twin_data).encode())

    def _serve_html_dashboard(self):
        """Serve a interface 3D de elite do Digital Twin (Three.js)."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SOLPI-OS | DIGITAL TWIN 3D</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <style>
                body { margin: 0; background: #000; color: #0f0; font-family: 'Courier New', monospace; overflow: hidden; }
                #ui { position: absolute; top: 20px; left: 20px; background: rgba(0,20,0,0.8); padding: 20px; border: 1px solid #0f0; border-radius: 5px; pointer-events: none; }
                .metric { margin-bottom: 10px; font-size: 14px; }
                .value { color: #fff; font-weight: bold; }
                #title { position: absolute; bottom: 20px; width: 100%; text-align: center; font-size: 24px; letter-spacing: 5px; text-shadow: 0 0 10px #0f0; }
                #loading { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); font-size: 20px; }
            </style>
        </head>
        <body>
            <div id="ui">
                <div class="metric">KERNEL: <span class="value" id="k-ver">BOOTING...</span></div>
                <div class="metric">UPTIME: <span class="value" id="uptime">0s</span></div>
                <div class="metric">NEURAL LOAD: <span class="value" id="load">0</span></div>
                <div class="metric">PREDICTION: <span class="value" id="pred">CALCULATING...</span></div>
                <div class="metric">STATE: <span class="value" id="state">SYNCING</span></div>
            </div>
            <div id="title">SOLPI-OS SINGULARITY v80.2</div>
            <div id="loading">INICIALIZANDO MOTOR GRÁFICO...</div>

            <script>
                let scene, camera, renderer, brain_sphere, particles;
                
                function init() {
                    document.getElementById('loading').style.display = 'none';
                    scene = new THREE.Scene();
                    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                    renderer = new THREE.WebGLRenderer({ antialias: true });
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    document.body.appendChild(renderer.domElement);

                    // Representação do Núcleo Neural
                    const geometry = new THREE.IcosahedronGeometry(2, 2);
                    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
                    brain_sphere = new THREE.Mesh(geometry, material);
                    scene.add(brain_sphere);

                    // Partículas de Dados (Rede)
                    const pCount = 500;
                    const pGeometry = new THREE.BufferGeometry();
                    const pMaterial = new THREE.PointsMaterial({ color: 0x00ff00, size: 0.05 });
                    const pCoords = new Float32Array(pCount * 3);
                    for(let i=0; i<pCount*3; i++) pCoords[i] = (Math.random() - 0.5) * 10;
                    pGeometry.setAttribute('position', new THREE.BufferAttribute(pCoords, 3));
                    particles = new THREE.Points(pGeometry, pMaterial);
                    scene.add(particles);

                    camera.position.z = 5;
                    animate();
                    setInterval(updateData, 2000);
                }

                function animate() {
                    requestAnimationFrame(animate);
                    brain_sphere.rotation.y += 0.01;
                    brain_sphere.rotation.x += 0.005;
                    particles.rotation.y -= 0.002;
                    renderer.render(scene, camera);
                }

                async function updateData() {
                    try {
                        const res = await fetch('/api/twin_data');
                        const data = await res.json();
                        
                        document.getElementById('k-ver').innerText = data.kernel.version;
                        document.getElementById('uptime').innerText = data.kernel.uptime;
                        document.getElementById('load').innerText = data.neural_load;
                        document.getElementById('pred').innerText = data.infrastructure.prediction;
                        
                        // Pulsação baseada na carga
                        const scale = 1 + (data.neural_load * 0.2);
                        brain_sphere.scale.set(scale, scale, scale);
                        
                        // Cor baseada em alerta
                        if(data.infrastructure.prediction.includes('⚠️')) {
                            brain_sphere.material.color.setHex(0xff0000);
                        } else {
                            brain_sphere.material.color.setHex(0x00ff00);
                        }
                    } catch(e) { console.error("Erro Twin:", e); }
                }

                window.addEventListener('resize', () => {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                });

                init();
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

class SOLPIGateway:
    """
    PACOTE 2200: DEVELOPER GATEWAY v80.2
    Interface visual e API do SOLPI-OS.
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
            print(f"🌐 [DEVELOPER]: Dashboard 3D Ativo em http://localhost:{self.port}")
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
