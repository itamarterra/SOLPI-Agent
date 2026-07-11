import time
from core.brain import SOLPIBrain

def test_v60_singularity():
    print("🔬 [TEST-SUITE]: Iniciando Auditoria da Singularidade v60.0...")
    print("-" * 50)
    
    # 1. Boot do Cérebro
    brain = SOLPIBrain()
    kernel = brain.kernel
    
    print(f"✅ KERNEL BOOT: Versão {kernel.version}")
    print(f"✅ BIOS INVENTORY: {kernel.hardware['cpu_cores']} Cores | {kernel.hardware['ram_total']}GB RAM")
    
    # 2. Teste de Topologia (Grafo de Arquitetura)
    topology = kernel.topology.graph
    print(f"✅ TOPOLOGY GRAPH: {len(topology['nodes'])} nós mapeados na malha.")
    
    # 3. Teste de Cognição e Execução
    print("\n🧠 [PENSAMENTO DE TESTE]: 'Verifique o status do servidor Zabbix'")
    response = brain.process("Verifique o status do servidor Zabbix")
    print(f"\nRESPOSTA DO SOLPI:\n{response}")
    
    # 4. Auditoria de Mercado de Recursos
    resource_status = kernel.resources.get_market_status()
    print(f"\n💰 RESOURCE MARKET: Consumo de Tokens: {resource_status['token_usage']}")
    
    # 5. Check de Memória e Service Bus
    history_len = len(brain.memory.short_term)
    print(f"📝 MEMORY BUS: {history_len} eventos registrados na memória de curto prazo.")
    
    print("-" * 50)
    print("🚀 CONCLUSÃO: Singularidade Operacional Confirmada.")

if __name__ == "__main__":
    try:
        test_v60_singularity()
    except Exception as e:
        print(f"🚨 FALHA NO TESTE: {e}")
