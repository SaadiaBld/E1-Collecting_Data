import sqlite3
import os

# Build the absolute path to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tweets.db')

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch all tweets
cursor.execute("SELECT id, text, cleaned_text, created_at FROM tweets")
rows = cursor.fetchall()

# Print the tweets
for row in rows:
    print(f"ID: {row[0]}\nOriginal Text: {row[1]}\nCleaned Text: {row[2]}\nCreated At: {row[3]}\n---")

conn.close()

