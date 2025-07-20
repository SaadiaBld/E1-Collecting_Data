import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

username = "LeroyMerlinFr"  # Sans le @

user = client.get_user(username=username)
print(f"ID de @{username} : {user.data.id}")
