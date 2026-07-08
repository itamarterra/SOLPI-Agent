import os
import importlib
import inspect

class DiscoveryEngine:
    """
    O Motor de Autodescoberta do SOLPI OS.
    Escanear e registra dinamicamente Agentes, Ferramentas e Plugins.
    """
    def __init__(self, registry, memory):
        self.registry = registry
        self.memory = memory
        self.capability_graph = {}

    def discover_all(self):
        print("🔍 [DISCOVERY]: Iniciando varredura de capacidades...")
        self._scan_agents()
        self._scan_skills()
        self._build_capability_graph()
        return self.capability_graph

    def _scan_agents(self):
        agents_path = "agents"
        for file in os.listdir(agents_path):
            if file.endswith("_agent.py") and file != "base_agent.py":
                module_name = f"agents.{file[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and name.endswith("Agent") and name != "BaseAgent":
                            # Instancia para disparar o register_tools
                            instance = obj(self.memory, self.registry)
                            print(f"✅ [DISCOVERY]: Agente detectado -> {name}")
                except Exception as e:
                    print(f"❌ [DISCOVERY]: Falha ao carregar agente {file}: {e}")

    def _scan_skills(self):
        skills_path = "skills"
        if os.path.exists(skills_path):
            skills = [d for d in os.listdir(skills_path) if os.path.isdir(os.path.join(skills_path, d))]
            for skill in skills:
                print(f"📦 [DISCOVERY]: Skill detectada -> {skill}")

    def _build_capability_graph(self):
        """Constrói o mapa de 'Quem sabe fazer o quê'."""
        tools = self.registry.list_all()
        for key, info in tools.items():
            agent = info['agent']
            if agent not in self.capability_graph:
                self.capability_graph[agent] = []
            self.capability_graph[agent].append(info['name'])
        print(f"🕸️ [CAPABILITY GRAPH]: {len(self.capability_graph)} agentes mapeados.")
