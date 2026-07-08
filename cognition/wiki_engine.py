import os
import json
from cognition.llm_engine import LLMEngine

class OmniWiki:
    """
    A Enciclopédia Global do SOLPI OMNI.
    Mapeia comandos da internet e os transforma em habilidades locais.
    """
    def __init__(self, memory):
        self.memory = memory
        self.llm = LLMEngine()
        self.wiki_path = "knowledge/wiki/"

    def learn_new_command(self, query):
        """Busca o comando na 'Internet' (via LLM/Search) e o cataloga."""
        print(f"🌐 [WIKI]: Pesquisando 'Como executar: {query}' na base global...")
        
        # 1. Consulta o Cérebro Global (Simulando busca em StackOverflow/Docs)
        prompt = f"""
        Você é o Pesquisador do SOLPI OMNI. 
        Encontre o comando exato de terminal (Windows/Linux) ou script para: {query}
        Retorne no formato JSON:
        {{
            "command_name": "nome_curto",
            "syntax": "comando --params",
            "description": "o que faz",
            "platform": "windows/linux/cloud"
        }}
        """
        res = self.llm.chat([{"role": "user", "content": prompt}])
        
        try:
            command_data = json.loads(res['choices'][0]['message']['content'])
            self._save_to_wiki(command_data)
            return command_data
        except:
            return None

    def _save_to_wiki(self, data):
        filename = f"{self.wiki_path}{data['command_name']}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"📚 [WIKI]: Comando '{data['command_name']}' imortalizado na enciclopédia.")

    def search_wiki(self, term):
        """Procura na nossa enciclopédia local antes de ir para a internet."""
        for file in os.listdir(self.wiki_path):
            if term.lower() in file.lower():
                with open(os.path.join(self.wiki_path, file), "r") as f:
                    return json.load(f)
        return None
