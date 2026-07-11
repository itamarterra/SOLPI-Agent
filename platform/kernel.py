import os
from datetime import datetime
from platform.bus import SOLPIServiceBus
from platform.bios import SOLPIBIOS
from platform.scheduler import SOLPITaskScheduler
from platform.storage import SOLPIStorage
from platform.topology import SOLPITopologyManager
from platform.resources import SOLPIResourceManager

class SOLPIKernel:
    """
    PACOTE 0001: SOLPI-OS META KERNEL v60.0
    Núcleo de Singularidade com Consciência de Topologia e Mercado de Recursos.
    """
    def __init__(self):
        self.start_time = datetime.now()
        self.version = "60.0-SINGULARITY"
        
        # 1. Sistema Nervoso e BIOS
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
