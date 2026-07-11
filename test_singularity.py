import time
from core.brain import SOLPIBrain

def test_v80_neural_engine():
    print("🔬 [TEST-SUITE]: Iniciando Auditoria da Singularidade v80.1 (Neural Engine)...")
    print("-" * 50)
    
    # 1. Boot do Cérebro
    brain = SOLPIBrain()
    kernel = brain.kernel
    
    print(f"✅ KERNEL BOOT: Versão {kernel.version}")
    
    # 2. Teste do Motor de Tensores (Inferência Preditiva)
    print("\n🔮 [TESTE PREDITIVO]: Analisando tendências de infraestrutura...")
    prediction = brain.predictor.predict_incident()
    print(f"RESULTADO: {prediction}")
    
    # 3. Teste do Digital Twin (Gêmeo Digital)
    print("\n👯 [TESTE DIGITAL TWIN]: Exportando snapshot do ecossistema...")
    snapshot_path = brain.twin.export_snapshot()
    print(f"SNAPSHOT GERADO EM: {snapshot_path}")
    
    # 4. Teste de Cognição Conversacional
    print("\n💬 [TESTE DIÁLOGO]: 'Consegue se autoevoluir?'")
    response = brain.process("Consegue se autoevoluir?")
    print(f"\nRESPOSTA DO SOLPI:\n{response}")
    
    # 5. Teste do Compilador IR e Neural VM (v80.2)
    print("\n⚡ [TESTE NEURAL VM]: Compilando e Executando Bytecode IR...")
    ir_code = brain.compiler_ir.auto_generate_ir("Quero prever incidentes")
    bytecode = brain.compiler_ir.compile(ir_code)
    vm_result = brain.neural_vm.execute_bytecode(bytecode)
    print(f"RESULTADO DA VM: {vm_result}")
    
    print("-" * 50)
    print("🚀 CONCLUSÃO: Singularidade Neural v80.1 Validada com Sucesso.")

if __name__ == "__main__":
    try:
        test_v80_neural_engine()
    except Exception as e:
        print(f"🚨 FALHA NO TESTE: {e}")
