import os
import threading
import time
from dotenv import load_dotenv
from core.brain import SOLPIBrain
from core.api_gateway import SOLPIGateway

load_dotenv()

class SOLPIOS:
    """
    SOLPI-OS: ENTERPRISE AI OPERATING SYSTEM (v37.0)
    Gerenciador Central com API Gateway e Event Bus.
    """
    def __init__(self):
        self.brain = SOLPIBrain()
        self.gateway = SOLPIGateway(self.brain) # Gateway Ativo
        self.active = True

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"🚀 SOLPI-OS ENTERPRISE v37.0 (Kernel: {self.brain.kernel.version})")
        print("=" * 60)
        print(f"STATUS: OPERACIONAL | GATEWAY: PORTA 8090 | BUS: ATIVO")
        print("=" * 60)
        
        # 1. Inicia API Gateway
        self.gateway.start()
        
        # 2. Inicia Monitoramento Proativo
        threading.Thread(target=self.proactive_monitor, daemon=True).start()

        while self.active:
            try:
                user_input = input("\n[SOLPI-OS] 👤 Itamar: ").strip()
                if user_input.lower() in ['exit', 'shutdown', 'poweroff']: break
                
                response = self.brain.process(user_input)
                print(f"\n[SOLPI-OS] 🧠 AI-RUNTIME:\n{response}")

            except KeyboardInterrupt: break
            except Exception as e: print(f"🚨 KERNEL PANIC: {e}")

    def proactive_monitor(self):
        while self.active:
            self.brain.heartbeat_check()
            time.sleep(300)

if __name__ == "__main__":
    os_instance = SOLPIOS()
    os_instance.run()
