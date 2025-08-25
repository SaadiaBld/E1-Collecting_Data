import sqlite3
import re
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tweets.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add the cleaned_text column if it doesn't exist
try:
    cursor.execute("ALTER TABLE tweets ADD COLUMN cleaned_text TEXT")
except sqlite3.OperationalError:
    # The column already exists
    pass

#nettoyer les tweets
def clean_text(tweet):
    tweet = re.sub(r'@\w+', '', tweet) #supprime les mentions @
    tweet = re.sub(r"http\S+|www\S+", '', tweet)  # Supprimer les liens
    tweet = tweet.replace("vs", "vous").replace("jms", "jamais")  # Remplacer abréviations
    tweet = re.sub(r'[^\w\s]', '', tweet)  # Supprimer ponctuation excessive
    return tweet.strip()

abbr_dict = {
    "vs": "vous",
    "jms": "jamais",
    "tjrs": "toujours",
    "tjs": "toujours",
    "tt": "tout",
    "pq": "pourquoi",
    "c": "c'est",
    "qd": "quand"
}

def expand_abbreviations(tweet):
    words = tweet.split()
    words = [abbr_dict[word] if word in abbr_dict else word for word in words]
    return " ".join(words)

def preprocess_tweet(tweet):
    tweet = tweet.lower()
    tweet = clean_text(tweet)
    tweet = expand_abbreviations(tweet)
    return tweet

# Fetch tweets that haven't been cleaned yet
cursor.execute("SELECT id, text FROM tweets WHERE cleaned_text IS NULL")
rows = cursor.fetchall()

for row in rows:
    tweet_id, text = row
    cleaned_text = preprocess_tweet(text)
    cursor.execute("UPDATE tweets SET cleaned_text = ? WHERE id = ?", (cleaned_text, tweet_id))

conn.commit()
conn.close()

print(f"{len(rows)} tweets cleaned and updated in the database.")
