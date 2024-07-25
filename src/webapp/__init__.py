from src.webapp.discordapi.api import DiscordApi
from src.models import Model
from dotenv import load_dotenv

discord_api = DiscordApi()
db = Model()
load_dotenv("../../.env")
