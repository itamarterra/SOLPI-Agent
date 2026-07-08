import os
from cognition.orchestrator import Orchestrator
from cognition.world_model import WorldModel

def test_trinity_fusion():
    print("="*80)
    print("🚀 [TRINITY FUSION TEST]: Iniciando Verificação de Unificação SOLPI OS v6.0")
    print("="*80)

    orchestrator = Orchestrator()
    world = WorldModel(orchestrator.memory)
    world_state = world.update_state()

    # Cenários de Teste para cada Motor
    scenarios = [
        {
            "name": "Fuso 1: Engenharia e Segurança (Claude)",
            "input": "Revise o código do kernel.py e faça uma auditoria de segurança",
            "expected_agent": "ClaudeAgent"
        },
        {
            "name": "Fuso 2: Operações Complexas (Hermes)",
            "input": "Configure um novo projeto de automação industrial com setup de banco de dados e logs",
            "expected_agent": "HermesAgent"
        },
        {
            "name": "Fuso 3: Interface e Visão (OpenClaw)",
            "input": "Faça uma varredura na tela, localize o menu de configurações e me notifique no WhatsApp",
            "expected_agent": "OpenClawAgent"
        },
        {
            "name": "Fuso 4: Automação Simples (Local)",
            "input": "Abra o google e pesquise sobre a cotação do dólar",
            "expected_agent": "BrowserAgent"
        }
    ]

    results = []

    for scenario in scenarios:
        print(f"\n🔹 TESTANDO: {scenario['name']}")
        print(f"💬 Prompt: '{scenario['input']}'")
        
        # Gera o plano
        task_tree = orchestrator.workflow.generate_task_tree(scenario['input'], world_state)
        
        # Verifica o agente delegado na primeira tarefa
        delegated_agent = task_tree['branches'][0]['agent']
        print(f"🎯 Agente Delegado: {delegated_agent}")

        if delegated_agent == scenario['expected_agent']:
            print("✅ SUCESSO: Roteamento correto.")
            results.append(True)
        else:
            print(f"❌ FALHA: Esperava {scenario['expected_agent']}, mas recebeu {delegated_agent}")
            results.append(False)

    print("\n" + "="*80)
    if all(results):
        print("🏆 [RESULTADO FINAL]: UNIFICAÇÃO TRINITY COMPLETA E FUNCIONAL!")
        print("O SOLPI OS v6.0 agora responde como um organismo único.")
    else:
        print("⚠️ [RESULTADO FINAL]: UNIFICAÇÃO COM PONTOS DE ATENÇÃO.")
    print("="*80)

if __name__ == "__main__":
    test_trinity_fusion()
