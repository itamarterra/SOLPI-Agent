import queue
import threading

class SOLPIEventBus:
    """
    PACOTE 2205: EVENT BUS v1.0
    Sistema de mensageria assíncrona para orquestração modular.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.queue = queue.Queue()
        self.subscribers = {}
        self.active = True
        
    def publish(self, event_type, data):
        """Publica um evento para o sistema (Etapa 1500)."""
        self.kernel.log_event("EVENT_BUS", f"Publicando: {event_type}")
        self.queue.put({"type": event_type, "data": data})

    def subscribe(self, event_type, callback):
        """Inscreve um módulo para ouvir um evento."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def start_listening(self):
        """Thread que processa a fila de eventos (Etapa 2204)."""
        def run():
            while self.active:
                event = self.queue.get()
                etype = event["type"]
                if etype in self.subscribers:
                    for cb in self.subscribers[etype]:
                        cb(event["data"])
                self.queue.task_done()
        
        threading.Thread(target=run, daemon=True).start()
