# Especificação Arquitetural: SOLPI OS v6.0 (Cognitive Engine)

## 1. Mudança de Paradigma
- **Antigo:** Entrada -> IF/ELSE -> Comando -> Resposta.
- **Novo:** Entrada -> Conversational Engine -> LLM (Brain) -> Intent -> Plan -> Execution -> Resposta.

## 2. O Cérebro (LLM Engine)
O LLM Engine é o único tomador de decisão. Ele deve:
- Receber o `Contexto do Mundo` (World Model).
- Receber o `Catálogo de Ferramentas` (Tool Registry).
- Decidir se o objetivo requer ação ou apenas conversa.

## 3. Contratos de Interface (The V6 Protocol)

### A. Ferramenta (Tool Contract)
Toda ferramenta deve ser descrita em JSON:
```json
{
  "name": "string",
  "description": "string",
  "parameters": {"type": "object", "properties": {...}},
  "risk": "low|medium|high"
}
```

### B. Agente (Agent Contract)
Todo agente deve implementar:
- `get_capabilities() -> List[Tool]`
- `execute(tool_name, params) -> Result`

### C. Decisão (Decision Logic)
O sistema deve classificar a intenção em: `CONVERSATION`, `GOAL`, `QUERY`.

## 4. O Fluxo de Controle
1. **User Input** capturado pelo `ConversationEngine`.
2. **LLM Engine** processa o input com o `System Prompt` (Persona + Capabilities).
3. Se `ACTION` for necessária:
    - **Planner** gera a `TaskTree`.
    - **Dispatcher** escolhe o agente via `CapabilityGraph`.
    - **Executor** roda e **Reflection** valida.
4. **LLM Engine** gera a resposta final baseada no resultado.
