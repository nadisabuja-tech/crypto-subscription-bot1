import sqlite3

conn = sqlite3.connect("data/bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    subscription INTEGER DEFAULT 0,
    expiry_date TEXT
)
""")

# পুরনো ডাটাবেসে expiry_date না থাকলে যোগ করবে
try:
    cursor.execute("ALTER TABLE users ADD COLUMN expiry_date TEXT")
except sqlite3.OperationalError:
    pass

conn.commit()

