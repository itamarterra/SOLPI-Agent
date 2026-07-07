import subprocess
import os
import time
import psutil
import pyautogui
from datetime import datetime

class AgentTools:
    """
    MOTOR PROTEGIDO: Impede travamentos de hardware e loops infinitos.
    """

    @staticmethod
    def execute_shell(command):
        """Executa comandos com TIMEOUT rigoroso para não travar o PC."""
        try:
            # Proteção: Não deixa o comando rodar para sempre
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=15 # Máximo 15 segundos por comando
            )
            return {"stdout": result.stdout, "stderr": result.stderr, "success": result.returncode == 0}
        except subprocess.TimeoutExpired:
            return {"error": "Comando interrompido por segurança (Timeout)", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}

    @staticmethod
    def check_pc_health():
        """Verifica se o PC está aguentando o tranco."""
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        if cpu > 90 or ram > 95:
            return False, f"CPU: {cpu}% | RAM: {ram}%"
        return True, "Healthy"

    @staticmethod
    def speak(text):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except: pass

    @staticmethod
    def log_evolution(message, log_type="evolution"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/{log_type}.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
            
    @staticmethod
    def git_sync(message="Auto-sync"):
        # Usa o caminho absoluto que descobrimos antes
        git = r'"C:\Program Files\Git\cmd\git.exe"'
        subprocess.run(f"{git} add .", shell=True)
        subprocess.run(f'{git} commit -m "{message}"', shell=True)
        subprocess.run(f"{git} push origin main", shell=True)
        return "Sincronizado."
