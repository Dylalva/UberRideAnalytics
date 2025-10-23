import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='predictions.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                input_data TEXT,
                prediction TEXT,
                probabilities TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_prediction(self, input_data, prediction, probabilities):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (input_data, prediction, probabilities)
            VALUES (?, ?, ?)
        ''', (json.dumps(input_data), prediction, json.dumps(probabilities)))
        conn.commit()
        conn.close()
    
    def get_all_predictions(self, limit=100):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, timestamp, input_data, prediction, probabilities
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()
        
        predictions = []
        for row in results:
            predictions.append({
                'id': row[0],
                'timestamp': row[1],
                'input_data': json.loads(row[2]),
                'prediction': row[3],
                'probabilities': json.loads(row[4])
            })
        return predictions
