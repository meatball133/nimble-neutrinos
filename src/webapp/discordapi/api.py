from os import getenv

from dotenv import load_dotenv
from flask import url_for
from requests import Session
from requests.auth import HTTPBasicAuth


class DiscordApi:
    def __init__(self):
        self.base_url = 'https://discord.com/api/v10'
        self.rsession = Session()
        load_dotenv()
        self.auth = HTTPBasicAuth(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))
        self.rsession.headers = {
            "User-Agent": "CordPics"
        }
        # FIXME don't hardcode this!!!!
        self.oauth_url = "https://discord.com/oauth2/authorize?client_id=1263403750056263741&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauthme&scope=guilds+identify"

    def get_oauth_tokens(self, code: str) -> dict:
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': url_for('authorizer', _external=True),
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = self.rsession.post(self.base_url + '/oauth2/token', data=data, headers=headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def get_user_info(self, token: str) -> dict:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.rsession.get(self.base_url + '/users/@me', headers=headers)
        response.raise_for_status()
        return response.json()

    def get_user_guilds(self, token: str) -> list[dict]:
        headers = {
            'Authorization': f"Bearer {token}"
        }
        response = self.rsession.get(self.base_url + '/users/@me/guilds', headers=headers)
        response.raise_for_status()
        return response.json()

    def get_channel_info(self, channel_id: str) -> dict:
        headers = {
            'Authorization': f"Bot {getenv('BOT_TOKEN')}",
        }
        response = self.rsession.get(self.base_url + f'/channels/{channel_id}', headers=headers)
        response.raise_for_status()
        return response.json()
