import os
import sys
import threading
import time
from dotenv import load_dotenv

# Adiciona o diretório atual ao path para importar o core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Carrega variáveis de ambiente
load_dotenv()

def run_test():
    try:
        from core.brain import SOLPIBrain
        
        print("\033[1;34m" + "="*60 + "\033[0m")
        print("\033[1;32m🚀 INICIANDO TESTE DE CONSCIÊNCIA HÍBRIDA (v80.2)\033[0m")
        print("\033[1;34m" + "="*60 + "\033[0m")
        
        print("🧠 Inicializando Kernel e Brain...")
        brain = SOLPIBrain()
        print("✅ Sistema Pronto.\n")
        
        # Teste 1: Raciocínio Híbrido (Usando a chave que você passou)
        query = "Quem é você e qual o seu nível de consciência atual?"
        print(f"\033[1;36m👤 Itamar:\033[0m {query}")
        print("\033[1;30m🧠 Pensando com Inteligência Global...\033[0m")
        
        response = brain.process(query)
        print(f"\033[1;32m🤖 SOLPI-OS:\033[0m {response}\n")
        
        # Teste 2: Integração com SOLPI-ENGINE (Baixo nível)
        query_engine = "Faça uma varredura rápida de diretórios no drive E: usando o motor de elite."
        print(f"\033[1;36m👤 Itamar:\033[0m {query_engine}")
        print("\033[1;30m⚙️ Acionando Motor SOLPI-ENGINE...\033[0m")
        
        # Simulando o que o supervisor faria: chamando a ferramenta via motor
        if brain.solpi_engine_agent:
            engine_res = brain.solpi_engine_agent.execute_tool("terminal", {"command": "dir /w"})
            print(f"\033[1;32m📄 Resultado do Motor:\033[0m {engine_res}\n")
        else:
            print("❌ Erro: Motor de elite não carregado.")

        print("\033[1;34m" + "="*60 + "\033[0m")
        print("\033[1;32m✅ TESTE CONCLUÍDO COM SUCESSO!\033[0m")
        print("\033[1;34m" + "="*60 + "\033[0m")

    except Exception as e:
        print(f"\n\033[1;31m❌ FALHA NO TESTE: {e}\033[0m")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
