from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NASA_API_KEY = os.getenv("NASA_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL")
LAVALINK_SV_PW = os.getenv("LAVALINK_SV_PW")