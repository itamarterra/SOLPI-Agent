import os
import sys
from dotenv import load_dotenv
from cognition.orchestrator import Orchestrator
from cognition.discovery_engine import DiscoveryEngine
from telemetry.monitor import OSMonitor

class SOLPI_OS:
    """
    O Kernel do SOLPI OS v5.0.
    Arquitetura baseada em Descoberta e Gráfico de Capacidades.
    """
    def __init__(self):
        self.version = "5.0.0-PRO"
        load_dotenv()
        
        # 1. HARDWARE & TELEMETRY
        self.monitor = OSMonitor()
        
        # 2. COGNITIVE CORE INITIALIZATION
        self.orchestrator = Orchestrator()
        self.orchestrator.monitor = self.monitor
        
        # 3. DISCOVERY SEQUENCE (O pulo do gato v5)
        self.discovery = DiscoveryEngine(self.orchestrator.registry, self.orchestrator.memory)
        
    def boot(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*65)
        print(f"🛰️  [KERNEL]: BOOTING SOLPI OS v{self.version}")
        print("="*65)
        
        # Executa a descoberta de tudo o que existe no sistema
        self.orchestrator.capabilities = self.discovery.discover_all()
        
        # Carrega Contexto e Memória
        print(f"🧠 [CORE]: Context & Memory Loaded.")
        print(f"🛡️  [SEC]: Security Gatekeeper Standing By.")
        print(f"📊 [OBS]: Telemetry Monitor Online.")
        print("="*65)
        
        self.orchestrator.voice.speak("SOLPI OS v5 inicializado. Sistema de descoberta concluiu o mapeamento de capacidades.")

    def run(self):
        self.boot()
        print(f"✨ [SYSTEM]: SOLPI OS Ready. Commands: 'objetivo', 'status', 'sair'")
        
        while True:
            try:
                user_input = input("\n👤 [ITAMAR]: ").strip()
                if not user_input:
                    user_input = self.orchestrator.voice.listen()
                    if not user_input: continue

                if user_input.lower() in ["exit", "sair", "shutdown"]:
                    sys.exit(0)

                response = self.orchestrator.solve(user_input)
                print(f"\n🤖 [SOLPI OS]: {response}")

            except Exception as e:
                print(f"⚠️ [SYSTEM ALERT]: {e}")

if __name__ == "__main__":
    system = SOLPI_OS()
    system.run()
