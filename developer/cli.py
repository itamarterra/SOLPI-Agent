import sys

class SOLPICLI:
    """
    PACOTE 2300: SOLPI COMMAND LINE v1.0
    Interface administrativa para controle direto via terminal.
    """
    def __init__(self, brain):
        self.brain = brain

    def handle_command(self, args):
        if not args: return
        cmd = args[0].lower()
        
        if cmd == "status":
            print(f"🖥️ SOLPI-OS v{self.brain.kernel.version}")
            print(f"🔋 Uptime: {self.brain.kernel.get_uptime()}")
            print(f"🧠 State: {self.brain.state_manager.get_state()}")
            
        elif cmd == "train":
            print("🚀 Iniciando ciclo de aprendizado manual...")
            self.brain.scheduler.schedule(self.brain.learning.start, priority=1, name="ManualTraining")
            
        elif cmd == "twin":
            print(f"🌐 Link Digital Twin: http://localhost:8090/twin")

        elif cmd == "audit":
            print("🛡️ Iniciando Auditoria de Auto-Arquitetura...")
            print(self.brain.architecture.scan_architecture())

        else:
            print(f"❓ Comando desconhecido: {cmd}")
