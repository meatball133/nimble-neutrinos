from dotenv import load_dotenv
from gunicorn.app.wsgiapp import WSGIApplication
from src.models import Model

db_model = Model()


class CordPicsApp(WSGIApplication):
    def __init__(self, app_uri, options=None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


def run_webapp():
    options = {
        "bind": "localhost:8000",  # TODO definitely do not hardcode this lmao
    }
    CordPicsApp("webapp.webapp:app", options).run()


if __name__ == "__main__":
    load_dotenv("../.env")  # TODO custom configs and maybe don't hardcode this?
    run_webapp()
