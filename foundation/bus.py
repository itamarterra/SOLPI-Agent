import queue
import threading
import time
import uuid

class SOLPIMessage:
    def __init__(self, sender, topic, payload, correlation_id=None):
        self.id = str(uuid.uuid4())[:8]
        self.correlation_id = correlation_id or self.id
        self.timestamp = time.time()
        self.sender = sender
        self.topic = topic
        self.payload = payload

class SOLPIServiceBus:
    """
    PACOTE 9400: AI SERVICE BUS v60.0
    Barramento compatível com orquestração distribuída e legado.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.queue = queue.Queue()
        self.subscribers = {}
        self.responses = {}
        self.active = True
        self._start_engine()

    def publish(self, topic, payload, sender="SYSTEM", correlation_id=None):
        """Publica mensagem. Topic e Payload são obrigatórios."""
        msg = SOLPIMessage(sender, topic, payload, correlation_id)
        self.queue.put(msg)
        return msg.id

    def subscribe(self, topic, callback):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def request(self, topic, payload, sender="SYSTEM", timeout=5):
        corr_id = self.publish(topic, payload, sender)
        start = time.time()
        while time.time() - start < timeout:
            if corr_id in self.responses:
                return self.responses.pop(corr_id)
            time.sleep(0.01)
        return {"status": "TIMEOUT"}

    def _start_engine(self):
        def run():
            while self.active:
                try:
                    msg = self.queue.get(timeout=1)
                    # Notifica assinantes
                    if msg.topic in self.subscribers:
                        for cb in self.subscribers[msg.topic]:
                            try: cb(msg)
                            except: pass
                    # Gerencia Respostas
                    if msg.topic == "RESPONSE":
                        self.responses[msg.correlation_id] = msg.payload
                    self.queue.task_done()
                except queue.Empty: continue
        threading.Thread(target=run, daemon=True).start()
