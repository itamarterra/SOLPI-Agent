import os
import sys
from dotenv import load_dotenv
from cognition.orchestrator import Orchestrator

class SOLPI_OS:
    """
    O Kernel do SOLPI OS v5.0.
    O Sistema Operacional Autônomo Evolutivo.
    """
    def __init__(self):
        self.version = "5.0.0-EVOLUTION"
        load_dotenv()
        self.orchestrator = Orchestrator()
        self._boot_message()

    def _boot_message(self):
        print("="*60)
        print(f"🚀 [BOOT]: SOLPI OS v{self.version}")
        print(f"🧠 [AI CORE]: Self-Improvement Engine v1.0 Active")
        print(f"🏪 [MARKET]: Plugin and Skill Manager Online")
        print(f"💻 [ENG]: Programming Agent ready for evolution")
        print("="*60)
        self.orchestrator.voice.speak(f"SOLPI versão 5 em operação. Estou pronto para evoluir, Comandante Itamar.")

    def run(self):
        print(f"✨ [SYSTEM]: SOLPI OS Ready. Commands: 'objetivo', 'status', 'marketplace'.")
        
        while True:
            try:
                user_input = input("\n👤 [ITAMAR]: ").strip()
                
                if not user_input:
                    user_input = self.orchestrator.voice.listen()
                    if not user_input: continue

                if user_input.lower() in ["exit", "sair", "shutdown"]:
                    sys.exit(0)

                # Ciclo de Autonomia Total e Evolução
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
