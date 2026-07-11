import sys
import os

print("--- DEBUG BOOT START ---")
try:
    print("Tentando importar foundation.kernel...")
    from foundation.kernel import SOLPIKernel
    print("OK")
    
    print("Tentando importar foundation.config...")
    from foundation.config import SOLPIConfig
    print("OK")

    print("Tentando importar core.brain...")
    from core.brain import SOLPIBrain
    print("OK")

    print("Tentando inicializar SOLPIBrain...")
    brain = SOLPIBrain()
    print("OK")

    print("Tentando importar developer.gateway...")
    from developer.gateway import SOLPIGateway
    print("OK")

    print("Boot Debug concluído com sucesso. Nenhum erro crítico de importação.")

except Exception as e:
    print(f"!!! ERRO DETECTADO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
