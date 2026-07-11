import queue
import threading
import time
import uuid

class SOLPIMessage:
    """Esquema de mensagem padronizado para o Service Bus."""
    def __init__(self, sender, topic, payload, correlation_id=None):
        self.id = str(uuid.uuid4())
        self.correlation_id = correlation_id or self.id
        self.timestamp = time.time()
        self.sender = sender
        self.topic = topic
        self.payload = payload

class SOLPIServiceBus:
    """
    PACOTE 9400: AI SERVICE BUS v1.0
    Sistema de mensageria de alta performance para orquestração de IA.
    Implementa o padrão Pub/Sub e Request/Response entre motores.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.queue = queue.Queue()
        self.subscribers = {}
        self.responses = {} # Para o padrão Request/Response
        self.active = True
        self._start_engine()

    def publish(self, sender, topic, payload, correlation_id=None):
        """Publica uma mensagem no barramento."""
        msg = SOLPIMessage(sender, topic, payload, correlation_id)
        self.kernel.log_event("SERVICE_BUS", f"[{topic}] {sender} -> Mensagem Enviada ({msg.id[:8]})")
        self.queue.put(msg)
        return msg.id

    def subscribe(self, topic, callback):
        """Inscreve um serviço para ouvir um tópico específico."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def request(self, sender, topic, payload, timeout=5):
        """Padrão Request/Response: Envia e aguarda uma resposta."""
        corr_id = self.publish(sender, topic, payload)
        start_wait = time.time()
        
        while time.time() - start_wait < timeout:
            if corr_id in self.responses:
                return self.responses.pop(corr_id)
            time.sleep(0.05)
        
        return {"status": "TIMEOUT", "error": "Resposta não recebida a tempo."}

    def _start_engine(self):
        """Inicia a thread de processamento do barramento."""
        def run():
            while self.active:
                try:
                    msg = self.queue.get(timeout=1)
                    # 1. Entrega para assinantes do tópico
                    if msg.topic in self.subscribers:
                        for callback in self.subscribers[msg.topic]:
                            callback(msg)
                    
                    # 2. Se for uma resposta, armazena para o solicitante
                    if msg.topic == "RESPONSE":
                        self.responses[msg.correlation_id] = msg.payload
                        
                    self.queue.task_done()
                except queue.Empty:
                    continue
        
        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self.active = False
