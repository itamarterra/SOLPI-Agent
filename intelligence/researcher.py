import os

class SOLPIResearcher:
    """
    PACOTE 1000: RESEARCH PARSER v1.0
    Vigia a pasta E:\SOLPI-RESEARCH em busca de inspiração técnica.
    """
    def __init__(self, research_dir="E:/SOLPI-RESEARCH"):
        self.research_dir = research_dir

    def scan_for_patterns(self, query):
        """Busca implementações específicas com limite de profundidade (v40.0)."""
        print(f"🔬 [RESEARCHER]: Escaneando biblioteca (Busca Rápida): '{query}'")
        found_files = []
        if not os.path.exists(self.research_dir): return []

        # Limita a busca para não travar o PC
        max_files_to_scan = 50
        scanned = 0
        
        for root, _, files in os.walk(self.research_dir):
            if scanned >= max_files_to_scan: break
            
            # Pula pastas gigantescas ou irrelevantes
            if any(x in root for x in [".git", "node_modules", "__pycache__", "datasets"]): continue

            for f in files:
                if f.endswith(('.py', '.cpp')):
                    scanned += 1
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as content:
                            if query.lower() in content.read().lower():
                                found_files.append(f"{f} ({os.path.basename(root)})")
                                if len(found_files) >= 3: return found_files
                    except: pass
        
        return found_files
