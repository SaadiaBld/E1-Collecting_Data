import tweepy
import dotenv
import os
import pandas as pd

# Charger les variables d'environnement
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
dotenv.load_dotenv(dotenv_path)
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authentification avec Twitter (OAuth 2.0)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Charger le fichier CSV existant (s'il y en a un)
csv_file = "tweets_leroymerlin_livraison.csv"
try:
    df_old = pd.read_csv(csv_file, dtype={"ID": str})  # Lire le CSV
    existing_ids = set(df_old["ID"])  # Récupérer les IDs existants pour éviter les doublons
except FileNotFoundError:
    df_old = pd.DataFrame(columns=["ID", "Texte", "Date"])  # Fichier vide
    existing_ids = set()

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
                tweet_data.append([tweet.id, tweet.text, tweet.created_at])
            else:
                print(f"Tweets ignorés: {tweet.text}")

    if tweet_data:
        df_temp = pd.DataFrame(tweet_data, columns=["ID", "Texte", "Date"])

        # Concaténer les anciens et nouveaux tweets et sauvegarder
        df_final = pd.concat([df_old, df_temp], ignore_index=True)
        df_final.to_csv(csv_file, index=False, encoding="utf-8")

        print(f"{len(df_temp)} nouveaux tweets ajoutés à {csv_file} !")
    else:
        print("Aucun nouveau tweet trouvé.")
else:
    print("Aucun tweet trouvé.")
