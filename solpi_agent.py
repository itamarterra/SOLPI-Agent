import os
import threading
import time
import sys
import subprocess
from dotenv import load_dotenv

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 🟢 AUTO-RECOVERY: Se não estivermos no .venv, tentamos re-lançar o script usando o venv correto
venv_python = os.path.abspath(os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe"))
if os.path.exists(venv_python) and sys.executable.lower() != venv_python.lower():
    print("🔄 Detectado lançamento fora do ambiente virtual. Redirecionando...")
    # Garante que o processo filho rode no diretório correto do projeto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run([venv_python] + sys.argv, cwd=os.getcwd())
    sys.exit(result.returncode)

try:
    from core.brain import SOLPIBrain
except ImportError as e:
    print(f"\n\033[1;31m❌ ERRO CRÍTICO DE AMBIENTE: {e}\033[0m")
    print("-" * 60)
    print("O módulo 'torch' ou outra dependência não foi encontrado.")
    print("\n👉 AÇÃO RECOMENDADA:")
    print("1. Feche esta janela.")
    print("2. Execute o arquivo 'INICIAR_SOLPI.bat' (ele vai consertar o ambiente).")
    print("3. NÃO abra o arquivo 'solpi_agent.py' diretamente.")
    print("-" * 60)
    input("Pressione Enter para sair...")
    sys.exit(1)

load_dotenv()

class SOLPIOS:
    """
    SOLPI-OS: ENTERPRISE AI OPERATING SYSTEM v80.2 (Singularity Elite)
    Interface Terminal Minimalista e Conversacional.
    """
    def __init__(self):
        print("⚙️ Inicializando Kernel SOLPI...")
        self.brain = SOLPIBrain()
        self.active = True

    def run(self):
        # Tenta limpar a tela
        try: os.system('cls' if os.name == 'nt' else 'clear')
        except: pass

        k_ver = self.brain.kernel.version
        
        print(f"\033[1;32m🚀 SOLPI-OS SINGULARITY v{k_ver}\033[0m")
        print("\033[1;34m" + "=" * 60 + "\033[0m")
        print(f"ESTADO: \033[1;32mPRONTO\033[0m | DRIVE E: \033[1;32mCONECTADO\033[0m | SEC: \033[1;32mON\033[0m")
        print(f"WEB UI: \033[1;36mhttp://localhost:8095\033[0m")
        print("\033[1;34m" + "=" * 60 + "\033[0m")
        
        # 1. Inicia API Gateway e Dashboard 3D
        try:
            self.brain.gateway.start()
        except Exception as ge:
            print(f"⚠️ Aviso: Falha ao iniciar Dashboard: {ge}")

        print("\n(Digite 'sair' para encerrar a sessão)\n")

        while self.active:
            try:
                # Entrada do Usuário com estilo
                user_input = input(f"\033[1;36m👤 Itamar:\033[0m ").strip()

                if not user_input: continue
                if user_input.lower() in ['sair', 'exit', 'shutdown', 'stop']:
                    print("\nEncerrando consciência SOLPI... Até logo, Arquiteto.")
                    self.active = False
                    break
                
                # Feedback de pensamento discreto
                print("\033[1;30m🧠 Pensando...\033[0m", end="\r")

                # Processamento
                response = self.brain.process(user_input)
                
                # Limpa a linha de pensamento
                print(" " * 40, end="\r")
                print(f"{response}\n")

            except KeyboardInterrupt:
                print("\nEncerrando via teclado...")
                break
            except Exception as e: 
                print(f"\n\033[1;31m🚨 ERRO DE NÚCLEO: {e}\033[0m")
                self.brain.kernel.log_event("CRITICAL", f"Panic: {e}")

if __name__ == "__main__":
    try:
        os_instance = SOLPIOS()
        os_instance.run()
    except Exception as init_error:
        print(f"\n\033[1;31m❌ FALHA FATAL NO BOOT: {init_error}\033[0m")
        import traceback
        traceback.print_exc()
        input("\nO sistema travou. Pressione Enter para fechar a janela...")
