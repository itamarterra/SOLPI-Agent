import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório atual ao path para importar o core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Carrega variáveis de ambiente
load_dotenv()

def run_test():
    try:
        from core.brain import SOLPIBrain
        
        print("\033[1;34m" + "="*60 + "\033[0m")
        print("\033[1;32m🚀 TESTANDO PROTOCOLO DE REFLEXÃO (v80.2)\033[0m")
        print("\033[1;34m" + "="*60 + "\033[0m")
        
        brain = SOLPIBrain()
        
        query = "Faça uma auto-reflexão e analise como podemos melhorar nossa comunicação com base nos manuais de 2025."
        print(f"\033[1;36m👤 Itamar:\033[0m {query}\n")
        
        response = brain.process(query)
        
        print(f"\033[1;32m🤖 RELATÓRIO DE AUTO-REFLEXÃO:\033[0m\n")
        print(response)
        
        print("\n\033[1;34m" + "="*60 + "\033[0m")

    except Exception as e:
        print(f"\n\033[1;31m❌ FALHA NO TESTE: {e}\033[0m")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
