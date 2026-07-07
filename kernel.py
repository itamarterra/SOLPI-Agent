import os
import sys
from dotenv import load_dotenv
from cognition.orchestrator import Orchestrator

class SOLPI_OS:
    """
    O Kernel do SOLPI OS v4.5.
    Suporte nativo a Voz, Visão e Auto-Recuperação.
    """
    def __init__(self):
        self.version = "4.5.0-INTEGRATED"
        load_dotenv()
        self.orchestrator = Orchestrator()
        self._boot_message()

    def _boot_message(self):
        print("="*60)
        print(f"🚀 [BOOT]: SOLPI OS v{self.version}")
        print(f"🧠 [AI CORE]: Integrated Brain Active")
        print(f"🎤 [VOICE]: Mic and Speakers Online")
        print(f"👁️  [VISION]: OCR and Object Detection Ready")
        print("="*60)
        self.orchestrator.voice.speak("Sistemas online. Estou pronto, Comandante Itamar.")

    def run(self):
        print(f"✨ [SYSTEM]: SOLPI OS Ready. Commands: 'objetivo', 'status', ou Pressione ENTER para falar.")
        
        while True:
            try:
                user_input = input("\n👤 [ITAMAR]: ").strip()
                
                # Se der ENTER vazio, usa o microfone
                if not user_input:
                    user_input = self.orchestrator.voice.listen()
                    if not user_input: continue

                if user_input.lower() in ["exit", "sair", "shutdown"]:
                    sys.exit(0)

                # Ciclo de Autonomia Total
                response = self.orchestrator.solve(user_input)
                print(f"\n🤖 [SOLPI OS]: {response}")

            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                print(f"⚠️ [CRITICAL]: {e}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    system = SOLPI_OS()
    system.run()
