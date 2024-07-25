import os

from flask import Flask

from src.config.db import engine
from src.webapp import endpoints
from src.models import Model
from src.webapp.discordapi.api import DiscordApi
from dotenv import load_dotenv

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.add_url_rule('/', view_func=endpoints.mainpage)
app.add_url_rule('/view', view_func=endpoints.gallery)
app.add_url_rule('/manage', view_func=endpoints.management)
app.add_url_rule('/login', view_func=endpoints.login)
app.add_url_rule('/authme', view_func=endpoints.authorizer)

if __name__ == '__main__':
    app.run(debug=True)  # FIXME don't forget to remove debug=True later.
