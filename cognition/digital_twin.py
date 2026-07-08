import json
import os
import platform
import psutil
from datetime import datetime

class DigitalTwin:
    """
    O Gêmeo Digital do SOLPI OS v6.0 (Trinity Edition).
    Mantém um espelhamento virtual do PC do Comandante Itamar e da infraestrutura.
    Funciona como uma 'Sandbox Mental' para prever colisões sistêmicas.
    """
    def __init__(self, memory):
        self.memory = memory
        self.state = {
            "local_pc": {
                "os": platform.system(),
                "node": platform.node(),
                "cores": os.cpu_count(),
                "active_processes": [],
                "open_ports": [],
                "critical_files": [
                    "C:/SOLPI-Agent/kernel.py",
                    "C:/SOLPI-Agent/cognition/orchestrator.py",
                    "C:/SOLPI-Agent/.env"
                ]
            },
            "infrastructure": {},
            "last_update": None
        }

    def refresh_local_state(self):
        """Captura o estado real do PC para atualizar o gêmeo digital."""
        print("🖇️ [DIGITAL TWIN]: Sincronizando espelhamento do PC local...")
        
        # 1. Mapeamento de Processos (Top 5 por CPU)
        try:
            procs = sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
            self.state["local_pc"]["active_processes"] = [p.info['name'] for p in procs]
        except: pass

        # 2. Mapeamento de Portas (Conexões ativas)
        try:
            conns = psutil.net_connections()
            self.state["local_pc"]["open_ports"] = list(set([c.laddr.port for c in conns if c.status == 'LISTEN']))
        except: pass

        self.state["last_update"] = datetime.now().isoformat()
        return self.state

    def simulate_action(self, agent_name, action_description):
        """
        Realiza o 'Pre-Flight Check'. 
        Simula a ação no gêmeo digital antes de permitir a execução física.
        """
        print(f"🔮 [DIGITAL TWIN]: Simulando '{action_description}' via {agent_name}...")
        
        prediction = {
            "safe": True,
            "risk_score": 0,
            "warnings": [],
            "expected_impact": "Estável"
        }

        # Regras de Colisão Sistêmica
        act_lower = action_description.lower()
        
        # 1. Detecção de Interferência em Arquivos Críticos
        for critical in self.state["local_pc"]["critical_files"]:
            if critical.lower() in act_lower and any(x in act_lower for x in ["delete", "remove", "sobrescrever"]):
                prediction["safe"] = False
                prediction["risk_score"] = 100
                prediction["warnings"].append(f"PROTEÇÃO TRINITY: Tentativa de alteração no núcleo vital -> {critical}")

        # 2. Detecção de Sobrecarga
        cpu_usage = psutil.cpu_percent()
        if cpu_usage > 90:
            prediction["risk_score"] += 40
            prediction["warnings"].append("ALERTA DE CARGA: CPU acima de 90%. Risco de congelamento do Kernel.")

        # 3. Regra de Especialidade
        if agent_name == "WindowsAgent" and "registry" in act_lower:
            prediction["risk_score"] += 60
            prediction["warnings"].append("RISCO DE CONFIGURAÇÃO: Alterações no registro do Windows podem exigir reinicialização.")

        if prediction["risk_score"] > 80:
            prediction["expected_impact"] = "Crítico"
        elif prediction["risk_score"] > 30:
            prediction["expected_impact"] = "Moderado"

        return prediction

    def sync_external_infra(self, zabbix_data):
        """Integra dados de servidores externos ao gêmeo digital."""
        for host in zabbix_data:
            self.state["infrastructure"][host['name']] = host
        return self.state
