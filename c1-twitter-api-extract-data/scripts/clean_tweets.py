import pandas as pd
import re, string

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

# Charger les tweets depuuis csv
csv_file = "tweets_leroymerlin_livraison.csv"
df = pd.read_csv(csv_file, dtype={"ID": str})

# Ajouter une colonne avec le tweet nettoyé
df["tweet_nettoye"] = df["Texte"].apply(preprocess_tweet)

# Sauvegarder les deux versions dans un CSV
df.to_csv("tweets_nettoyes.csv", index=False, encoding="utf-8")
