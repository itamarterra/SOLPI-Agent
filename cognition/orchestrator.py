import time
from cognition.memory import SOLPIMemory
from cognition.world_model import WorldModel
from cognition.llm_engine import LLMEngine
from cognition.intent_analyzer import IntentAnalyzer
from cognition.planner import Planner
from cognition.executor import Executor
from tools.voice_core import VoiceCore

class Orchestrator:
    """
    O Sistema Nervoso do SOLPI OS v6.0.
    Conecta o Cérebro (LLM) aos Músculos (Agentes).
    """
    def __init__(self):
        self.llm = LLMEngine()
        self.intent = IntentAnalyzer(self.llm)
        self.memory = SOLPIMemory()
        self.world = WorldModel(self.memory)
        self.planner = Planner(self.memory)
        self.executor = Executor(self.memory)
        self.voice = VoiceCore()

    def solve(self, user_input):
        # 1. PERCEPÇÃO
        world_state = self.world.update_state()
        
        # 2. ANALISAR INTENÇÃO (O fim do if/else)
        intent = self.intent.analyze(user_input, world_state)
        print(f"🎯 [INTENT]: {intent}")

        # 3. DECISÃO DE FLUXO
        if intent == "CONVERSATION":
            return self._handle_conversation(user_input)
        
        elif intent in ["GOAL", "TROUBLESHOOTING"]:
            self.voice.speak("Entendido. Vou planejar a execução.")
            # O LLM agora dita o plano (via Planner)
            plan = self.planner.create_plan(user_input, world_state)
            result = self.executor.run_plan(plan)
            return self._handle_conversation(f"O usuário pediu '{user_input}' e o resultado da execução foi: {result}")

        return self._handle_conversation(user_input)

    def _handle_conversation(self, text):
        messages = [
            {"role": "system", "content": "Você é o SOLPI OS, um Sistema Operacional Cognitivo. Responda de forma técnica e prestativa."},
            {"role": "user", "content": text}
        ]
        res = self.llm.chat(messages)
        try:
            msg = res['choices'][0]['message']['content']
            self.voice.speak(msg)
            return msg
        except:
            return "Desculpe, meu cérebro está temporariamente offline."
