import subprocess
import os
import psutil
from security.gatekeeper import SecurityGatekeeper

class SystemTools:
    """Ferramentas de Interação com o Sistema Operacional."""
    
    @staticmethod
    def execute_shell(command):
        # Sanitização e Segurança via Gatekeeper
        clean_cmd = SecurityGatekeeper.sanitize_shell(command)
        safe, reason = SecurityGatekeeper.is_safe(clean_cmd)
        
        if not safe:
            return {"error": reason, "success": False}

        try:
            result = subprocess.run(
                clean_cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": str(e), "success": False}

    @staticmethod
    def get_resources():
        """Retorna uso de CPU e RAM."""
        return {
            "cpu": f"{psutil.cpu_percent()}%",
            "ram": f"{psutil.virtual_memory().percent}%"
        }
