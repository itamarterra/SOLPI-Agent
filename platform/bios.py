import psutil
import platform
import os
import torch

class SOLPIBIOS:
    """
    PACOTE 9500: AI BIOS v1.0
    Responsável pela detecção de hardware e validação de ambiente no boot.
    Detecta GPU, CPU, RAM e integridade de Drives.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.inventory = {}

    def boot_check(self):
        """Executa a varredura de hardware inicial."""
        self.kernel.log_event("BIOS", "Iniciando detecção de hardware...")
        
        self.inventory = {
            "os": platform.system(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
            "gpu_detected": torch.cuda.is_available(),
            "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None",
            "drive_e_status": os.path.exists("E:/")
        }
        
        status = "✅ BIOS OK" if self.inventory["drive_e_status"] else "⚠️ DRIVE E: MISSING"
        self.kernel.log_event("BIOS", f"Hardware: {self.inventory['cpu_cores']} Cores | {self.inventory['ram_total']}GB RAM | GPU: {self.inventory['gpu_name']}")
        
        return self.inventory
