import os

from dotenv import load_dotenv

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

username = os.getenv("MONGO_DB_USERNAME")
password = os.getenv("MONGO_DB_PASSWORD")
cluster = "cluster0.5okimuc.mongodb.net"

# Replace with your actual MongoDB Atlas connection string
connection_string = f"mongodb+srv://{username}:{password}@{cluster}/"
