import os
import threading
import time
import sys
from dotenv import load_dotenv

# Adiciona o diretório atual ao path para garantir que os domínios sejam encontrados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.brain import SOLPIBrain
from developer.gateway import SOLPIGateway

load_dotenv()

class SOLPIOS:
    """
    SOLPI-OS: ENTERPRISE AI OPERATING SYSTEM v70.0 (Hardened)
    Ponto de Entrada Unificado da Singularidade.
    """
    def __init__(self):
        # Inicializa o Cérebro (Que sobe o Kernel, BIOS e Service Bus)
        self.brain = SOLPIBrain()
        # Inicializa o Gateway no domínio Developer
        self.gateway = SOLPIGateway(self.brain)
        self.active = True

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        k_ver = self.brain.kernel.version
        
        print(f"🚀 SOLPI-OS SINGULARITY v{k_ver} (Enterprise Hardened)")
        print("=" * 65)
        print(f"KERNEL: ATIVO | BUS: OPERACIONAL | DRIVE E: CONECTADO | SEC: ON")
        print("=" * 65)
        
        # 1. Inicia API Gateway Externo
        self.gateway.start()
        
        # 2. Inicia Monitoramento de Telemetria e Previsão
        threading.Thread(target=self.proactive_monitor, daemon=True).start()

        while self.active:
            try:
                # Interface Humana
                user_input = input("\n[SOLPI-OS] 👤 Itamar: ").strip()
                if not user_input: continue
                if user_input.lower() in ['exit', 'shutdown', 'poweroff']: 
                    self.active = False
                    break
                
                print("🧠 [PROCESSANDO]...", end="\r")
                response = self.brain.process(user_input)
                
                # Feedback Limpo
                print(" " * 30, end="\r")
                print(f"\n{response}")

            except KeyboardInterrupt: break
            except Exception as e: 
                print(f"🚨 KERNEL PANIC: {e}")
                # Log do erro no domínio de Operações
                self.brain.kernel.log_event("CRITICAL", f"Panic: {e}")

    def proactive_monitor(self):
        """Monitora o ecossistema a cada 5 minutos."""
        while self.active:
            try:
                self.brain.heartbeat_check()
            except: pass
            time.sleep(300)

if __name__ == "__main__":
    try:
        os_instance = SOLPIOS()
        os_instance.run()
    except Exception as init_error:
        print(f"❌ FALHA NO BOOT: {init_error}")
