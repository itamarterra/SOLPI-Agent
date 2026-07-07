import sqlite3
import os
from datetime import datetime

class SOLPIMemory:
    def __init__(self, db_path="memory/aios_core.db"):
        self.db_path = db_path
        self.short_term_cache = {} # Memória de Sessão (Volátil)
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS long_term_mem USING fts5(content, layer, tags, timestamp UNINDEXED)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, objective TEXT, plan TEXT, result TEXT, status TEXT, execution_time FLOAT, timestamp DATETIME)''')
        conn.commit()
        conn.close()

    # Memória de Curto Prazo (Interconexão)
    def set_session_context(self, key, value):
        self.short_term_cache[key] = value
        print(f"🧠 [MEMÓRIA]: Contexto de sessão atualizado: {key} -> {value}")

    def get_session_context(self, key):
        return self.short_term_cache.get(key)

    def remember(self, content, layer="experience", tags=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO long_term_mem (content, layer, tags, timestamp) VALUES (?, ?, ?, ?)", (content, layer, tags, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def recall(self, query, layer=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM long_term_mem WHERE long_term_mem MATCH ? ORDER BY rank LIMIT 10", (query,))
        results = cursor.fetchall()
        conn.close()
        return [r[0] for r in results]

    def log_task(self, objective, plan, result, status, duration):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (objective, plan, result, status, execution_time, timestamp) VALUES (?, ?, ?, ?, ?, ?)", (objective, plan, result, status, duration, datetime.now().isoformat()))
        conn.commit()
        conn.close()
