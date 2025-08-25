import tweepy
import dotenv
import os
import sqlite3

# Charger les variables d'environnement
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
dotenv.load_dotenv(dotenv_path)
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authentification avec Twitter (OAuth 2.0)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Connexion à la base de données
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tweets.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Récupérer les IDs existants pour éviter les doublons
cursor.execute("SELECT id FROM tweets")
existing_ids = {row[0] for row in cursor.fetchall()}

# Construire la requête de recherche
query = ('("Leroy Merlin" OR @LeroyMerlinFR OR @leroymerlin) '
         '("livraison" OR "colis" OR "commande" OR "expédition" OR "transport") '
         '-"arnaque" -"escroquerie" -"millions" -"examen" -"Amazon" -"Zulon" '
         '-is:retweet lang:fr')

# Fonction de filtrage : garder seulement les tweets contenant certains mots-clés
def est_tweet_pertinent(texte):
    mots_cles = ["commande", "livraison", "colis", "remboursement", "expédition", "retard", "transporteur",'transport', ]
    return any(mot in texte.lower() for mot in mots_cles)

# Récupérer les tweets récents (max 25, pour respecter le quota de 100/mois gratuites))
tweets = client.search_recent_tweets(query=query, max_results=25, tweet_fields=["created_at", "author_id"], 
                                      expansions=["author_id"])

# Stocker les tweets dans une liste
tweet_data = []
leroy_merlin_ids = {"32358920"}  # IDs de Leroy Merlin pour éviter les doublons
if tweets.data:
    for tweet in tweets.data:
        if str(tweet.id) not in existing_ids:
            if str(tweet.author_id) in leroy_merlin_ids:
                continue
            if est_tweet_pertinent(tweet.text):
                tweet_data.append((str(tweet.id), tweet.text, str(tweet.created_at)))
            else:
                print(f"Tweets ignorés: {tweet.text}")

    if tweet_data:
        cursor.executemany("INSERT INTO tweets (id, text, created_at) VALUES (?, ?, ?)", tweet_data)
        conn.commit()
        print(f"{len(tweet_data)} nouveaux tweets ajoutés à la base de données !")
    else:
        print("Aucun nouveau tweet trouvé.")
else:
    print("Aucun tweet trouvé.")

conn.close()
