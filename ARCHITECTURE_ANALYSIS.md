# Análise de Arquitetura: SOLPI-AIOS (v2.0.0-Cognitive)

## 1. Visão Geral
O projeto atual é um assistente funcional baseado em Python com capacidades de execução de ferramentas (ferramentas de sistema, visão OCR, voz e integração de banco de dados). Embora poderoso, ele opera em um fluxo linear de "Comando -> Resposta". O objetivo desta transformação é implementar um loop de raciocínio recursivo (Reasoning Loop).

## 2. Pontos Fortes (Atual)
*   **Modularidade de Ferramentas:** O arquivo `core/tools.py` já separa bem as capacidades físicas do agente.
*   **Segurança Nativa:** O `SecurityGatekeeper` fornece uma camada de proteção essencial para um sistema autônomo.
*   **Memória Persistente:** O uso de SQLite FTS5 permite busca semântica rápida em histórico.
*   **Capacidade Sensorial:** Implementação funcional de OCR (Visão) e STT/TTS (Voz).

## 3. Problemas e Limitações
*   **Cérebro Reativo:** O `core/brain.py` utiliza cadeias de `if/elif`, o que impede o planejamento de tarefas complexas de múltiplos passos.
*   **Ausência de Orquestrador:** Não há distinção entre o agente que decide e o agente que executa.
*   **Falta de Reflexão:** O sistema não avalia se o comando executado atingiu o objetivo esperado.
*   **Dependência de Coordenadas:** O controle de GUI ainda é muito dependente de cliques em texto/coordenadas, faltando uma abstração de "objetos" de interface.

## 4. Proposta de Melhoria (Roadmap de Fases)

### Fase 1: Fundação Cognitiva (Curto Prazo)
*   Reestruturar `core/` para `cognition/`.
*   Implementar o **Orchestrator** como ponto de entrada único.
*   Introduzir o **Planner** para decomposição de objetivos em grafos de tarefas.
*   Implementar suporte básico ao **MCP (Model Context Protocol)**.

### Fase 2: Ecossistema de Multiagentes (Médio Prazo)
*   Criar a classe base `BaseAgent`.
*   Especializar os agentes: `WindowsAgent`, `BrowserAgent`, `GLPIAgent`, `ZabbixAgent`.
*   Implementar o **Tool Registry** dinâmico.

### Fase 3: Auto-Evolução e Observabilidade (Longo Prazo)
*   Módulo de **Reflection** para pós-execução.
*   Módulo de **Learning** para ajuste de pesos e experiências.
*   Dashboard de Observabilidade (Tempo, CPU, Taxa de Sucesso).

## 5. Próximos Passos Imediatos
1. Criar estrutura de diretórios `/cognition`.
2. Migrar lógica de `brain.py` para `orchestrator.py` e `reasoner.py`.
3. Implementar o sistema de Memória em 6 camadas (Short, Long, Knowledge, Conv, Task, Experience).
