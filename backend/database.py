import sqlite3

# This creates a local database file right inside your backend folder
DB_PATH = "chat_history.db"

def init_db():
    """Creates the database table if it doesn't exist yet."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT,
            ai_response TEXT,
            department TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_message(session_id, user_query, ai_response, department):
    """Saves a single back-and-forth chat into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (session_id, user_query, ai_response, department)
        VALUES (?, ?, ?, ?)
    ''', (session_id, user_query, ai_response, department))
    conn.commit()
    conn.close()

def get_history(session_id):
    """Retrieves all past messages for a specific user session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_query, ai_response FROM conversations 
        WHERE session_id = ? ORDER BY id ASC
    ''', (session_id,))
    history = cursor.fetchall()
    conn.close()
    return history