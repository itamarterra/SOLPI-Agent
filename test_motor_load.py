import os
import sys

# Simula o ambiente do solpi_agent.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.brain import SOLPIBrain
    print("🧠 Inicializando Brain...")
    brain = SOLPIBrain()
    print("✅ Brain inicializado.")
    
    if brain.solpi_engine_agent:
        print(f"🚀 Motor de Elite detectado.")
        
        # Teste de execução de ferramenta: 'terminal'
        print("🛠️ Executando teste de ferramenta: terminal(command='dir')")
        # terminal(command: str, background: bool = False)
        result = brain.solpi_engine_agent.execute_tool("terminal", {"command": "dir"})
        print(f"📄 Resultado do Motor:\n{result}")

    else:
        print("❌ Motor de Elite não carregado no Brain.")
        
except Exception as e:
    print(f"❌ Falha no teste: {e}")
    import traceback
    traceback.print_exc()
