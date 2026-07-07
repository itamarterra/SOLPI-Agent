# Especificação Técnica: SOLPI AI Core (v2.0)

## 1. O Fluxo de Pensamento (Cognitive Chain)
Todo objetivo recebido pelo Kernel deve obrigatoriamente passar pelas seguintes fases:
1.  **Entendimento:** Decomposição semântica e consulta à `SemanticMemory`.
2.  **Planejamento:** Criação de um grafo de tarefas via `WorkflowEngine`.
3.  **Raciocínio:** Escolha de Agentes e Ferramentas baseada em `KnowledgeMemory`.
4.  **Execução:** Delegação para o `AgentDispatcher`.
5.  **Verificação:** Validação sensorial (Vision) e lógica via `Reflection`.
6.  **Aprendizado:** Registro de falhas e sucessos na `ExperienceMemory`.

## 2. Contratos de Interface (Interfaces)
- **Agentes:** Devem implementar `execute(task) -> TaskResult`.
- **Ferramentas:** Devem fornecer metadados JSON (Input/Output/Permission).
- **Memória:** Deve suportar as 6 camadas (Conversation, Semantic, Experience, Task, Knowledge, Procedural).

## 3. Sensores Integrados
- **Vision Core:** OCR + Template Matching (OpenCV).
- **Voice Core:** STT/TTS como serviço sistêmico.
- **Computer Use:** Driver de controle de interface via acessibilidade e visão.
