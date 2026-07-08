import time
import threading
from datetime import datetime
from cognition.orchestrator import Orchestrator

class MissionScheduler:
    """
    Inspirado no Hermes Cron: Permite agendar objetivos estratégicos 
    usando linguagem natural ou tempo fixo.
    """
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.jobs = []
        self.active = True
        threading.Thread(target=self._scheduler_loop, daemon=True).start()

    def schedule_mission(self, time_str, objective):
        """Agenda uma missão (Ex: '22:00', 'Backup total')"""
        job = {
            "time": time_str,
            "objective": objective,
            "last_run": None
        }
        self.jobs.append(job)
        print(f"📅 [SCHEDULER]: Missão agendada para às {time_str}: {objective}")

    def _scheduler_loop(self):
        while self.active:
            now = datetime.now().strftime("%H:%M")
            for job in self.jobs:
                if job["time"] == now and job["last_run"] != datetime.now().date():
                    print(f"⏰ [SCHEDULER]: Disparando missão agendada -> {job['objective']}")
                    self.orchestrator.solve(job["objective"])
                    job["last_run"] = datetime.now().date()
            time.sleep(30) # Checa a cada 30 segundos
