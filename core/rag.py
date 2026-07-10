import os

class SOLPIRAGEngine:
    """
    PACOTE 2100: RAG ENGINE v1.0
    Recuperação e Ranking de conhecimento da pasta RESEARCH (Disco E:).
    """
    def __init__(self, research_dir="E:/SOLPI-RESEARCH"):
        self.research_dir = research_dir
        self.index = {}

    def retrieve(self, query):
        """Busca os 'Chunks' mais relevantes nos repositórios (Etapa 1402)."""
        print(f"🔍 [RAG]: Recuperando contexto de elite para '{query}'...")
        results = []
        
        # Simula busca vetorial/textual nos projetos clonados
        for root, _, files in os.walk(self.research_dir):
            for f in files:
                if f.endswith(('.py', '.cpp', '.md')):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as content:
                            text = content.read()
                            if query.lower() in text.lower():
                                # Retorna o arquivo e um trecho (Chunk - Etapa 1400)
                                start = text.lower().find(query.lower())
                                results.append({
                                    "source": f"{os.path.basename(root)}/{f}",
                                    "chunk": text[max(0, start-100):start+300]
                                })
                    except: pass
        return results[:3] # Retorna os 3 melhores (Etapa 1403)
