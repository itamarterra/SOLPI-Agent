import sys
import os

# Adiciona a raiz ao path
root = "E:/SOLPI-Agent"
sys.path.append(root)

print("🔍 [DEBUG]: Iniciando Diagnóstico de Importações...")

try:
    print("1. Testando foundation.kernel...")
    from foundation.kernel import SOLPIKernel
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

try:
    print("2. Testando intelligence.runtime...")
    from intelligence.runtime import SOLPINeuralRuntime
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

try:
    print("3. Testando execution.supervisor...")
    from execution.supervisor import SOLPISupervisor
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

try:
    print("4. Testando core.brain...")
    from core.brain import SOLPIBrain
    print("   ✅ OK")
    print("\n🚀 [BOOT TEST]: Tentando instanciar SOLPIBrain...")
    brain = SOLPIBrain()
    print("✅ Cérebro instanciado com sucesso!")
except Exception as e:
    print(f"❌ FALHA FATAL NO BRAIN: {e}")
    import traceback
    traceback.print_exc()
