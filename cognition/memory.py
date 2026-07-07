import sqlite3
import os
from datetime import datetime
import json

class SOLPIMemory:
    """
    MEMÓRIA SUPREMA: 7 Camadas de Consciência para o AI Core.
    """
    def __init__(self, db_path="memory/ai_core.db"):
        self.db_path = db_path
        self.cache = {
            "conversation": [], # Short-term
            "current_task": None
        }
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Semantic Memory (FTS5) - Busca por significado
        cursor.execute('CREATE VIRTUAL TABLE IF NOT EXISTS semantic USING fts5(content, tags, timestamp UNINDEXED)')
        
        # 2. Procedural Memory - Como fazer as coisas (Skills)
        cursor.execute('CREATE TABLE IF NOT EXISTS procedural (id INTEGER PRIMARY KEY, skill_name TEXT, steps TEXT, version TEXT)')
        
        # 3. Experience Memory - O que funcionou e o que falhou
        cursor.execute('CREATE TABLE IF NOT EXISTS experience (id INTEGER PRIMARY KEY, scenario TEXT, outcome TEXT, lessons TEXT)')
        
        # 4. Knowledge Memory - Fatos do mundo (GLPI, Zabbix, etc)
        cursor.execute('CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, key TEXT, value TEXT, category TEXT)')

        # 5. Task Memory - Histórico de execuções
        cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, objective TEXT, result TEXT, status TEXT)')

        # 6. Conversation Memory - Logs de chat
        cursor.execute('CREATE TABLE IF NOT EXISTS conversation (id INTEGER PRIMARY KEY, user_input TEXT, agent_response TEXT, timestamp DATETIME)')
        
        conn.commit()
        conn.close()

    def store_experience(self, scenario, outcome, lessons):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO experience (scenario, outcome, lessons) VALUES (?, ?, ?)", 
                       (scenario, outcome, json.dumps(lessons)))
        conn.commit()
        conn.close()

    def search_semantic(self, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM semantic WHERE semantic MATCH ? ORDER BY rank", (query,))
        return [r[0] for r in cursor.fetchall()]
