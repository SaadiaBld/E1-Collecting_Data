import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))

print("Chargement des tweets...")
subprocess.run(["python3", os.path.join(base_dir, "load_tweets.py")])

print("Nettoyage des tweets...")
subprocess.run(["python3", os.path.join(base_dir, "clean_tweets.py")])

print("Pipeline terminée avec succès !")
