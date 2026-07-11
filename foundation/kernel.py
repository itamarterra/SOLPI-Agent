import os
from datetime import datetime
from foundation.bus import SOLPIServiceBus
from foundation.bios import SOLPIBIOS
from foundation.scheduler import SOLPITaskScheduler
from foundation.storage import SOLPIStorage
from foundation.topology import SOLPITopologyManager
from foundation.resources import SOLPIResourceManager
from foundation.security import SOLPISecurity

class SOLPIKernel:
    """
    PACOTE 0001: SOLPI-OS META KERNEL v70.3 (Secure Singularity)
    Núcleo de Singularidade com Segurança Nativa e Zero Trust.
    """
    def __init__(self):
        self.start_time = datetime.now()
        self.version = "80.2-SINGULARITY"
        
        # 1. Inicializa Segurança ANTES de tudo
        self.security = SOLPISecurity(self)
        
        # 2. Inicializa Barramento e BIOS
        self.service_bus = SOLPIServiceBus(self)
        self.event_bus = self.service_bus
        self.bios = SOLPIBIOS(self)
        self.hardware = self.bios.boot_check()
        
        # 2. Infraestrutura Industrial (Blueprint 300)
        self.topology = SOLPITopologyManager(self) # Architecture Graph
        self.resources = SOLPIResourceManager(self) # Resource Market
        self.scheduler = SOLPITaskScheduler(self)
        self.storage = SOLPIStorage(self)
        
        # 3. Mapeia a Arquitetura no Boot
        self.malha = self.topology.scan_runtime_topology()
        
        self.log_event("KERNEL", f"SOLPI-OS {self.version} Meta-Kernel Ativo.")

    def log_event(self, layer, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{layer}] {event}\n"
        
        # 🟢 UPGRADE v70.6: Silenciamos o console para uma interface limpa
        # O log continua sendo gravado no arquivo kernel_events.log para auditoria
        # print(f"⚙️ [{layer}]: {event}")
            
        try:
            with open("kernel_events.log", "a", encoding="utf-8") as f:
                f.write(entry)
        except: pass

    def authorize(self, action):
        return True

    def get_uptime(self):
        return str(datetime.now() - self.start_time)
