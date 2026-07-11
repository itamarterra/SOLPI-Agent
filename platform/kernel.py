import os
from datetime import datetime
from platform.bus import SOLPIServiceBus
from platform.bios import SOLPIBIOS
from platform.scheduler import SOLPITaskScheduler
from platform.storage import SOLPIStorage

class SOLPIKernel:
    """
    PACOTE 0001: SOLPI-OS KERNEL v50.3
    O Núcleo central da plataforma. Gerencia o ciclo de vida de todos os domínios.
    Implementa BIOS, Service Bus, Scheduler e Storage.
    """
    def __init__(self):
        self.start_time = datetime.now()
        self.version = "50.3-ENTERPRISE"
        
        # 1. Inicializa o Barramento de Serviços (Sistema Nervoso)
        self.service_bus = SOLPIServiceBus(self)
        self.event_bus = self.service_bus
        
        # 2. Inicializa BIOS (Detecção de Hardware)
        self.bios = SOLPIBIOS(self)
        self.hardware = self.bios.boot_check()
        
        # 3. Inicializa Scheduler e Storage
        self.scheduler = SOLPITaskScheduler(self)
        self.storage = SOLPIStorage(self)
        
        self.log_event("KERNEL", f"SOLPI-OS {self.version} Bootloader concluído.")

    def log_event(self, layer, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{layer}] {event}\n"
        
        if layer != "LEARNING" or "concluído" in event:
            print(f"⚙️ [{layer}]: {event}")
            
        try:
            with open("kernel_events.log", "a", encoding="utf-8") as f:
                f.write(entry)
        except: pass

    def authorize(self, action):
        return True

    def get_uptime(self):
        return str(datetime.now() - self.start_time)
