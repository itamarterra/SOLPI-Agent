import os
import sys
from dotenv import load_dotenv
from cognition.orchestrator import Orchestrator
from cognition.discovery_engine import DiscoveryEngine
from telemetry.monitor import OSMonitor

class SOLPI_OS:
    """
    O Kernel do SOLPI OS v6.0.
    Sistema Operacional Híbrido: SOLPI Core + Hermes Engine.
    """
    def __init__(self):
        self.version = "6.0.0-HYBRID"
        load_dotenv()
        
        # 1. HARDWARE & TELEMETRY
        self.monitor = OSMonitor()
        
        # 2. COGNITIVE CORE INITIALIZATION
        self.orchestrator = Orchestrator()
        self.orchestrator.monitor = self.monitor
        
        # 3. DISCOVERY SEQUENCE
        self.discovery = DiscoveryEngine(self.orchestrator.registry, self.orchestrator.memory)
        
    def boot(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*65)
        print(f"🛰️  [KERNEL]: BOOTING SOLPI OS v{self.version}")
        print("="*65)
        
        # Executa a descoberta de tudo o que existe no sistema
        self.orchestrator.capabilities = self.discovery.discover_all()
        
        print(f"🧠 [CORE]: Cognitive Brain Unified.")
        print(f"🏛️  [EXT]: Hermes-Agent Core Integrated.")
        print(f"🛡️  [SEC]: Security Gatekeeper Active.")
        print(f"📊 [OBS]: Telemetry Monitor Online.")
        print("="*65)
        
        self.orchestrator.voice.speak("SOLPI OS v6 híbrido inicializado. O motor Hermes foi integrado ao nosso núcleo.")

    def run(self):
        self.boot()
        
        # ACIONA A VOLIÇÃO INICIAL
        from cognition.volition_engine import VolitionEngine
        volition = VolitionEngine(self.orchestrator.simulator.twin, self.orchestrator.memory)
        suggestion = volition.generate_autonomous_goal()
        
        print(f"✨ [SYSTEM]: Ready. Dê um objetivo ou use 'ajuda'.")
        print(f"💡 [INICIATIVA]: Comandante Itamar, eu sugiro uma missão: '{suggestion['goal']}'")
        self.orchestrator.voice.speak(f"Comandante, eu sugiro uma missão: {suggestion['goal']}")
        
        while True:
            try:
                user_input = input("\n👤 [ITAMAR]: ").strip()
                if not user_input:
                    user_input = self.orchestrator.voice.listen()
                    if not user_input: continue

                if user_input.lower() in ["exit", "sair", "shutdown"]:
                    sys.exit(0)

                response = self.orchestrator.solve(user_input)
                print(f"\n🤖 [SOLPI OS]:\n{response}")

            except Exception as e:
                print(f"⚠️ [SYSTEM ALERT]: {e}")

if __name__ == "__main__":
    # Garante que o sistema rode a partir do diretório raiz do SOLPI-Agent
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)
    sys.path.append(root_dir)

    system = SOLPI_OS()
    system.run()
