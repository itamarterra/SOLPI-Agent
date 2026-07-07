import os
import sys
from dotenv import load_dotenv
from cognition.orchestrator import Orchestrator

class SOLPI_OS:
    """
    O Kernel do SOLPI OS v6.0.
    Sistema Operacional de Inteligência Artificial Geral Unificado.
    """
    def __init__(self):
        self.version = "6.0.0-UNIFIED"
        load_dotenv()
        
        # O Orquestrador inicializa todos os sub-motores (Vision, Voice, Memory, Swarm, etc)
        self.orchestrator = Orchestrator()
        self._boot_sequence()

    def _boot_sequence(self):
        print("="*65)
        print(f"🛰️  [SYSTEM]: BOOTING SOLPI OS v{self.version}")
        print(f"🧠 [AI CORE]: LLM-Centric Brain v6.0 Online")
        print(f"🌍 [WORLD]: Situational Awareness v2.0 Active")
        print(f"🐝 [SWARM]: Swarm Intelligence Manager Online")
        print(f"🧬 [EXP]: Experience Distillation Engine Ready")
        print("="*65)
        self.orchestrator.voice.speak("SOLPI OS versão 6.0 ativado. Todos os sistemas estão unificados e prontos para o comando.")

    def shutdown(self):
        print("\n🛑 [KERNEL]: Shutting down SOLPI OS...")
        sys.exit(0)

    def run(self):
        print(f"✨ [SYSTEM]: Ready. Dê um objetivo estratégico ou pressione ENTER para falar.")
        
        while True:
            try:
                user_input = input("\n👤 [ITAMAR]: ").strip()
                
                # Suporte a Voz se der ENTER vazio
                if not user_input:
                    user_input = self.orchestrator.voice.listen()
                    if not user_input: continue

                if user_input.lower() in ["exit", "sair", "shutdown"]:
                    self.shutdown()

                # Ciclo Cognitivo Universal Unificado
                response = self.orchestrator.solve(user_input)
                print(f"\n🤖 [SOLPI OS]:\n{response}")

            except KeyboardInterrupt:
                self.shutdown()
            except Exception as e:
                print(f"⚠️ [SYSTEM ERROR]: {e}")

if __name__ == "__main__":
    # Garante que as pastas de log e memória existem
    os.makedirs("logs", exist_ok=True)
    os.makedirs("memory", exist_ok=True)

    os.system('cls' if os.name == 'nt' else 'clear')
    system = SOLPI_OS()
    system.run()
