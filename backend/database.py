import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "recruitment.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        jd_text TEXT,
        resume_name TEXT,
        match_percentage INTEGER,
        analysis_data TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_analysis(user_id, jd_text, resume_name, match_percentage, analysis_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO analysis_history (user_id, jd_text, resume_name, match_percentage, analysis_data)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, jd_text, resume_name, match_percentage, json.dumps(analysis_data)))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, jd_text, resume_name, match_percentage, created_at 
    FROM analysis_history 
    WHERE user_id = ? 
    ORDER BY created_at DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "jd_text": row[1],
            "resume_name": row[2],
            "match_percentage": row[3],
            "created_at": row[4]
        } for row in rows
    ]

def get_analysis_detail(analysis_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT analysis_data FROM analysis_history WHERE id = ?", (analysis_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return None

if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
