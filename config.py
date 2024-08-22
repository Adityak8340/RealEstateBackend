import os
from dotenv import load_dotenv

load_dotenv()

FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")