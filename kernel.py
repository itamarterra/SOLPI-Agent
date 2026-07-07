import os
import sys
from dotenv import load_dotenv
from cognition.orchestrator import Orchestrator
from telemetry.monitor import OSMonitor

class SOLPI_OS:
    """
    O Kernel do SOLPI OS v3.0.
    Sistema Operacional de Inteligência Artificial Geral.
    """
    def __init__(self):
        self.version = "3.0.0-COGNITIVE"
        load_dotenv()
        self.monitor = OSMonitor()
        self.orchestrator = Orchestrator()
        # Injeta o monitor no orquestrador para observabilidade
        self.orchestrator.monitor = self.monitor
        
        self._boot_message()

    def _boot_message(self):
        print("="*60)
        print(f"🚀 [BOOT]: SOLPI OS v{self.version}")
        print(f"🧠 [CORE]: Cognition Engine v2.0 Activated")
        print(f"🛡️  [SEC]: Security Gatekeeper Standing By")
        print(f"📊 [OBS]: Telemetry Monitor Online")
        print("="*60)

    def shutdown(self):
        print("\n🛑 [KERNEL]: Shutting down SOLPI OS...")
        sys.exit(0)

    def run(self):
        print(f"✨ [SYSTEM]: SOLPI OS Ready. Commands: 'objetivo [desc]', 'status', 'sair'")
        
        while True:
            try:
                user_input = input("\n👤 [ITAMAR]: ").strip()
                
                if not user_input: continue
                
                if user_input.lower() in ["exit", "sair", "shutdown"]:
                    self.shutdown()

                if user_input.lower() == "status":
                    metrics = self.monitor.get_system_metrics()
                    print(f"📊 [STATUS]: CPU: {metrics['cpu_usage']} | RAM: {metrics['memory_usage']} | Uptime: {metrics['uptime']}")
                    continue

                # Ciclo de Autonomia Total
                response = self.orchestrator.solve(user_input)
                print(f"\n🤖 [SOLPI OS]: {response}")

            except KeyboardInterrupt:
                self.shutdown()
            except Exception as e:
                print(f"⚠️ [CRITICAL]: {e}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    system = SOLPI_OS()
    system.run()
