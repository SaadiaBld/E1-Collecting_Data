import sqlite3
import os

# Build the absolute path to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tweets.db')

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)

# Create a cursor
cursor = conn.cursor()

# Create the tweets table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tweets (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
