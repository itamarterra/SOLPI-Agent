import time

class SOLPICognitiveProcess:
    """Representação de um processo mental ativo."""
    def __init__(self, pid, name, domain):
        self.pid = pid
        self.name = name
        self.domain = domain
        self.status = "ACTIVE"
        self.start_time = time.time()

class SOLPICognitiveProcessManager:
    """
    PACOTE 5700: COGNITIVE PROCESS MANAGER v51.0
    O "Task Manager" do cérebro. Monitora threads de pensamento, aprendizado e execução.
    Gerencia ciclos de 'Deep Sleep' (Consolidação) e 'High Alert' (Incidente).
    """
    def __init__(self, brain):
        self.brain = brain
        self.processes = {}
        self.next_pid = 1

    def spawn_thought(self, name, domain):
        pid = self.next_pid
        self.processes[pid] = SOLPICognitiveProcess(pid, name, domain)
        self.next_pid += 1
        self.brain.kernel.log_event("COGNITION", f"Novo Processo Mental [PID {pid}]: {name}")
        return pid

    def terminate_thought(self, pid):
        if pid in self.processes:
            self.processes[pid].status = "TERMINATED"
            del self.processes[pid]

    def get_brain_load(self):
        """Calcula carga cognitiva atual."""
        return len([p for p in self.processes.values() if p.status == "ACTIVE"])
