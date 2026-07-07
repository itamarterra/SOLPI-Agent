import os
import sys
from dotenv import load_dotenv
from cognition.orchestrator import Orchestrator

class SOLPI_OS:
    """
    O Kernel do SOLPI OS v4.0.
    O Sistema Operacional de Inteligência Artificial Geral.
    """
    def __init__(self):
        self.version = "4.0.0-AI-CORE"
        load_dotenv()
        self.orchestrator = Orchestrator()
        self._boot_sequence()

    def _boot_sequence(self):
        print("="*65)
        print(f"🛰️  [SYSTEM]: BOOTING SOLPI OS v{self.version}")
        print(f"🧠 [AI CORE]: Cognitive Engine v4.0 Online")
        print(f"🌍 [WORLD]: Situational Awareness Active")
        print(f"🧬 [EXP]: Experience Engine Distilling Wisdom")
        print(f"🌲 [WORKFLOW]: Task Tree Decomposer Stand-by")
        print("="*65)
        self.orchestrator.voice.speak("SOLPI AI CORE v4 ativo. Eu entendo, eu sinto e eu evoluo. Estou pronto, Comandante.")

    def shutdown(self):
        print("\n🛑 [KERNEL]: Shutting down SOLPI OS...")
        sys.exit(0)

    def run(self):
        print(f"✨ [SYSTEM]: SOLPI AI Core Ready. Dê seu objetivo estratégico.")
        
        while True:
            try:
                user_input = input("\n👤 [ITAMAR]: ").strip()
                if not user_input:
                    user_input = self.orchestrator.voice.listen()
                    if not user_input: continue

                if user_input.lower() in ["exit", "sair", "shutdown"]:
                    self.shutdown()

                # Ciclo Cognitivo de 12 Etapas
                response = self.orchestrator.solve(user_input)
                print(f"\n🤖 [SOLPI OS]: {response}")

            except KeyboardInterrupt:
                self.shutdown()
            except Exception as e:
                print(f"⚠️ [SYSTEM ALERT]: {e}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    system = SOLPI_OS()
    system.run()
