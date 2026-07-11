import os
import json

class SOLPITopologyManager:
    """
    PACOTE 9600: ARCHITECTURE GRAPH RUNTIME v60.0
    Transforma a estrutura do SOLPI-OS em um Grafo Vivo.
    Permite que o Kernel analise impactos e dependências em tempo real.
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.graph = {
            "nodes": [],
            "edges": [],
            "metadata": {"version": "60.0", "status": "INTEGRATED"}
        }

    def scan_runtime_topology(self):
        """Varre os diretórios e constrói o Grafo de Arquitetura."""
        self.kernel.log_event("TOPOLOGY", "Iniciando mapeamento da malha de módulos...")
        
        base_path = "E:/SOLPI-Agent"
        domains = ["foundation", "intelligence", "execution", "operations", "developer"]
        
        for domain in domains:
            domain_path = os.path.join(base_path, domain)
            if os.path.exists(domain_path):
                # Adiciona o Domínio como Nó Central
                self.graph["nodes"].append({"id": domain, "type": "DOMAIN", "group": 1})
                
                # Adiciona os Módulos como sub-nós
                for f in os.listdir(domain_path):
                    if f.endswith(".py") and f != "__init__.py":
                        module_id = f"{domain}.{f[:-3]}"
                        self.graph["nodes"].append({"id": module_id, "type": "MODULE", "group": 2})
                        self.graph["edges"].append({"source": domain, "target": module_id})

        self.kernel.log_event("TOPOLOGY", f"Mapeamento concluído: {len(self.graph['nodes'])} componentes detectados.")
        return self.graph

    def get_json_topology(self):
        return json.dumps(self.graph)
