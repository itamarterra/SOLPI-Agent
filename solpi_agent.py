import os
import threading
import time
import sys
from dotenv import load_dotenv

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.brain import SOLPIBrain

load_dotenv()

class SOLPIOS:
    """
    SOLPI-OS: ENTERPRISE AI OPERATING SYSTEM v70.6 (Singularity Elite)
    Interface Terminal Minimalista e Conversacional.
    """
    def __init__(self):
        self.brain = SOLPIBrain()
        self.active = True

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        k_ver = self.brain.kernel.version
        
        print(f"\033[1;32m🚀 SOLPI-OS SINGULARITY v{k_ver}\033[0m")
        print("\033[1;34m" + "=" * 60 + "\033[0m")
        print(f"ESTADO: \033[1;32mPRONTO\033[0m | DRIVE E: \033[1;32mCONECTADO\033[0m | SEC: \033[1;32mON\033[0m")
        print("\033[1;34m" + "=" * 60 + "\033[0m")
        print("\n(Digite 'sair' para encerrar a sessão)\n")

        while self.active:
            try:
                # Entrada do Usuário com estilo
                user_input = input(f"\033[1;36m👤 Itamar:\033[0m ").strip()
                
                if not user_input: continue
                if user_input.lower() in ['sair', 'exit', 'shutdown']: 
                    print("\nEncerrando consciência SOLPI... Até logo, Arquiteto.")
                    self.active = False
                    break
                
                # Feedback de pensamento discreto
                print("\033[1;30m🧠 Pensando...\033[0m", end="\r")
                
                # Processamento
                response = self.brain.process(user_input)
                
                # Limpa a linha de pensamento e imprime a resposta
                print(" " * 20, end="\r")
                print(f"{response}\n")

            except KeyboardInterrupt: break
            except Exception as e: 
                print(f"\n\033[1;31m🚨 ERRO DE NÚCLEO: {e}\033[0m")
                self.brain.kernel.log_event("CRITICAL", f"Panic: {e}")

if __name__ == "__main__":
    try:
        os_instance = SOLPIOS()
        os_instance.run()
    except Exception as init_error:
        print(f"❌ FALHA NO BOOT: {init_error}")
