import sqlite3
import os
from datetime import datetime
import json

class BrainMemory:
    """
    MEMÓRIA DO CÉREBRO: O motor de consciência do SOLPI OS.
    Renomeado para evitar conflitos com a pasta 'memory/'.
    """
    def __init__(self, db_path="memory/ai_brain.db"):
        self.db_path = db_path
        self.short_term = []
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Semantic Memory (FTS5)
        cursor.execute('CREATE VIRTUAL TABLE IF NOT EXISTS semantic USING fts5(content, tags, timestamp UNINDEXED)')
        
        # Experience Memory
        cursor.execute('CREATE TABLE IF NOT EXISTS experience (id INTEGER PRIMARY KEY, scenario TEXT, outcome TEXT, lessons TEXT)')
        
        # Task History
        cursor.execute('CREATE TABLE IF NOT EXISTS task_log (id INTEGER PRIMARY KEY AUTOINCREMENT, objective TEXT, result TEXT, status TEXT, timestamp DATETIME)')

        # Conversation History
        cursor.execute('CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY, user_input TEXT, agent_response TEXT, timestamp DATETIME)')
        
        conn.commit()
        conn.close()

    def record(self, content, layer="semantic", tags=""):
        """Grava uma informação na memória persistente."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO semantic (content, tags, timestamp) VALUES (?, ?, ?)",
                (content, tags, datetime.now().isoformat())
            )
            conn.commit()
        except Exception as e:
            print(f"⚠️ [MEMORY ERROR]: {e}")
        finally:
            conn.close()

    def search(self, query):
        """Busca na memória semântica."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT content FROM semantic WHERE semantic MATCH ? ORDER BY rank LIMIT 10", (query,))
            return [r[0] for r in cursor.fetchall()]
        except:
            return []
        finally:
            conn.close()

    def distill_experience(self, scenario, outcome, lessons):
        """Registra aprendizado de elite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO experience (scenario, outcome, lessons) VALUES (?, ?, ?)", 
                       (scenario, outcome, json.dumps(lessons)))
        conn.commit()
        conn.close()
