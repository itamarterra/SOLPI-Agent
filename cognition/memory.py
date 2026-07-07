import sqlite3
import os
from datetime import datetime
import json

class SOLPIMemory:
    """
    Gerenciador de Memória em 7 Camadas:
    1. Short Term (Sessão atual)
    2. Long Term (Persistência histórica)
    3. Semantic (Busca por similaridade/FTS5)
    4. Task (Histórico de planos e execuções)
    5. Experience (Aprendizados e reflexões)
    6. Conversation (Logs de interação)
    7. Knowledge (Base de fatos e ferramentas)
    """
    def __init__(self, db_path="memory/solpi_os.db"):
        self.db_path = db_path
        self.short_term = {} # Memória de Curto Prazo (Volátil)
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Camada Semântica e Long Term (FTS5 para busca rápida)
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS semantic_memory 
            USING fts5(content, layer, tags, timestamp UNINDEXED)
        ''')
        
        # Camada de Tarefas (Task Memory)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                objective TEXT,
                plan TEXT,
                result TEXT,
                status TEXT,
                duration FLOAT,
                timestamp DATETIME
            )
        ''')

        # Camada de Experiência (Experience Memory)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experience_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario TEXT,
                action_taken TEXT,
                outcome TEXT,
                lessons_learned TEXT,
                timestamp DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()

    # Operações de Curto Prazo
    def set_context(self, key, value):
        self.short_term[key] = value

    def get_context(self, key):
        return self.short_term.get(key)

    # Operações de Longo Prazo e Semântica
    def store(self, content, layer="knowledge", tags=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO semantic_memory (content, layer, tags, timestamp) VALUES (?, ?, ?, ?)",
            (content, layer, tags, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def search(self, query, layer=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if layer:
            cursor.execute(
                "SELECT content FROM semantic_memory WHERE semantic_memory MATCH ? AND layer = ? ORDER BY rank",
                (query, layer)
            )
        else:
            cursor.execute(
                "SELECT content FROM semantic_memory WHERE semantic_memory MATCH ? ORDER BY rank",
                (query,)
            )
        results = cursor.fetchall()
        conn.close()
        return [r[0] for r in results]

    # Registro de Experiência e Aprendizado
    def log_experience(self, scenario, action, outcome, lessons):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO experience_memory (scenario, action_taken, outcome, lessons_learned, timestamp) VALUES (?, ?, ?, ?, ?)",
            (scenario, action, outcome, json.dumps(lessons), datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
