import sqlite3
import os
from datetime import datetime, timedelta

class TemporalMemory:
    """
    Memória Temporal do SOLPI OS v5.2.
    Rastreia a evolução de métricas e estados ao longo do tempo para detectar tendências.
    """
    def __init__(self, db_path="memory/temporal_metrics.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                metric_name TEXT,
                value REAL,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def record_metric(self, source, name, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO metrics (source, metric_name, value, timestamp) VALUES (?, ?, ?, ?)",
            (source, name, value, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def get_trend(self, source, name, hours=24):
        """Analisa se a métrica está subindo, descendo ou estável."""
        start_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value FROM metrics WHERE source = ? AND metric_name = ? AND timestamp > ? ORDER BY timestamp ASC",
            (source, name, start_time)
        )
        values = [row[0] for r in cursor.fetchall()]
        conn.close()

        if len(values) < 2:
            return "Estável (Dados insuficientes)"
        
        diff = values[-1] - values[0]
        if diff > (values[0] * 0.2): # Aumento de 20%
            return "Tendência de Alta 📈"
        elif diff < -(values[0] * 0.2):
            return "Tendência de Baixa 📉"
        return "Estável ➡️"
