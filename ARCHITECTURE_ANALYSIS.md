# Arquitetura SOLPI OS: Sistema Operacional Cognitivo (v3.0.0)

## 1. Filosofia de Design
O SOLPI OS opera sob o princípio da **Cognição Proativa**. Diferente de sistemas tradicionais baseados em triggers, este sistema busca compreender o "estado desejado" do usuário e orquestra múltiplos agentes especializados para alcançá-lo, validando cada etapa e aprendendo com as falhas de hardware e software.

## 2. Estrutura de Diretórios (Layout Profissional)
```text
SOLPI-OS/
├── cognition/      # O Cérebro (Orchestrator, Reasoner, Planner, Reflection, Learning)
├── agents/         # Multiagentes Especializados (Windows, Docker, Browser, etc.)
├── tools/          # Plugins de hardware e sistema (antiga core/tools)
├── workflows/      # Definições de fluxos complexos (YAML/JSON)
├── memory/         # Memória Persistente e Vetorial (SQLite/FTS5)
├── knowledge/      # Base de conhecimento estática e dinâmica
├── integrations/   # Conectores externos (Shopify, Zabbix, GLPI)
├── security/       # Guardião de permissões e sanitização
├── telemetry/      # Observabilidade (CPU, RAM, Performance)
└── kernel.py       # O ponto de entrada (Bootstrapper)
```

## 3. RoadMap de Implementação (Fases)

### Fase 1: Kernel e Cognição (Atual)
*   Consolidar `orchestrator.py` como o Kernel do sistema.
*   Implementar o `ToolRegistry` como catálogo central de capacidades.
*   Migrar a segurança para o módulo `security/`.

### Fase 2: Domínio de Interface (Próxima)
*   Implementar o `BrowserAgent` com suporte a múltiplas abas.
*   Evoluir o `AutomationAgent` para reconhecimento de objetos via OpenCV.

### Fase 3: Governança e Observabilidade
*   Implementar telemetria em tempo real.
*   Sistema de permissões por nível de risco.

## 4. Decisões Arquiteturais
*   **Abstração de Ferramentas:** Agentes não chamam comandos shell diretamente; eles solicitam ao ToolRegistry.
*   **Memória em 7 Camadas:** Adição da camada Semântica para busca de similaridade.
