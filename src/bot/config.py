import os

from dotenv import load_dotenv

load_dotenv()


# Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
assert BOT_TOKEN is not None

# Developer options
TESTING_MODE = bool(os.getenv("TESTING_MODE"))
TESTING_BOT_TOKEN = os.getenv("TESTING_BOT_TOKEN") or BOT_TOKEN
if TESTING_MODE:
    assert TESTING_BOT_TOKEN is not None

# IDs
OWNER_IDS: tuple = (
	534651911903772674, # GetPsyched
	330028725553070090, # meatball
	1063920139713654825, # malik
	746807967650807810, # Jezz
	707977917485023376, # HiPeople
)

# PostgreSQL
class DB:
    def __init__(self):
        self.DATABASE = os.getenv("PGDATABASE")
        self.HOST = os.getenv("PGHOST")
        self.PASSWORD = os.getenv("PGPASSWORD")
        self.PORT = os.getenv("PGPORT")
        self.USER = os.getenv("PGUSER")

        for variable, value in self.__dict__.items():
            if value is None:
                raise Exception(f"PostgreSQL variable for `{variable}` is not set")

    @property
    def DSN(self):
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
