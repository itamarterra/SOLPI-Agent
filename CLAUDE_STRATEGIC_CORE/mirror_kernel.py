# 🛰️ KERNEL ESPELHO (CLAUDE CLONE)
# Este arquivo roda a MINHA lógica pura, para você comparar com o SOLPI.

from logic.reasoning_engine import ClaudeReasoning
from logic.communication_engine import ClaudeCommunication

class ClaudeClone:
    def __init__(self):
        self.brain = ClaudeReasoning()
        self.voice = ClaudeCommunication()
        self.version = "1.0.0-CLONE"

    def run(self):
        print("="*60)
        print(f"🧬 [MATRIZ CLAUDE]: CLONE OPERACIONAL v{self.version}")
        print("="*60)
        
        while True:
            cmd = input("\n👤 [ITAMAR]: ")
            if cmd.lower() in ["exit", "sair"]: break
            
            # Pensa como eu
            thought = self.brain.analyze_mission(cmd)
            
            # Fala como eu
            report = self.voice.format_response(thought)
            print(f"\n{report}")

if __name__ == "__main__":
    clone = ClaudeClone()
    clone.run()
