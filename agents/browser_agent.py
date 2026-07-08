import webbrowser
import time
from agents.base_agent import BaseAgent

class BrowserAgent(BaseAgent):
    """
    Agente especializado em navegação na internet e automação web.
    """
    def register_tools(self):
        if self.registry:
            self.registry.register("BrowserAgent", "open", "Abrir uma URL específica")
            self.registry.register("BrowserAgent", "search", "Pesquisar no Google ou YouTube")

    def execute(self, task_description):
        print(f"🌍 [BROWSER AGENT]: Processando -> {task_description}")
        task_lower = task_description.lower()
        
        if "youtube" in task_lower:
            if "pesquise" in task_lower or "busque" in task_lower:
                query = task_lower.split("por")[-1].strip()
                return self._search_youtube(query)
            return self._open_url("https://www.youtube.com")
            
        elif "google" in task_lower or "pesquise" in task_lower:
            query = task_lower.split("por")[-1].strip()
            return self._search_google(query)

        elif "site" in task_lower or "http" in task_lower:
            import re
            url = re.search(r"(https?://\S+)", task_description)
            if url:
                return self._open_url(url.group(0))
        
        return f"BrowserAgent: Entendi que devo '{task_description}', mas ainda estou aprendendo a interagir com este site específico."

    def _open_url(self, url):
        try:
            webbrowser.open(url)
            self.log_activity(f"Abriu a URL: {url}")
            return f"✅ Site aberto: {url}"
        except Exception as e:
            return f"❌ Erro ao abrir site: {str(e)}"

    def _search_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.log_activity(f"Pesquisou no YouTube por: {query}")
        return f"🎬 Pesquisando por '{query}' no YouTube..."

    def _search_google(self, query):
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.log_activity(f"Pesquisou no Google por: {query}")
        return f"🔍 Buscando por '{query}' no Google..."
