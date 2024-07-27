import os

from flask import Flask

from src.webapp import endpoints

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.add_url_rule('/', view_func=endpoints.mainpage)
app.add_url_rule('/view', view_func=endpoints.gallery)
app.add_url_rule('/manage', view_func=endpoints.management)
app.add_url_rule('/login', view_func=endpoints.login)
app.add_url_rule('/authme', view_func=endpoints.authorizer)
app.add_url_rule('/install', view_func=endpoints.install_redirect)
app.add_url_rule('/channels', view_func=endpoints.server_channels)
app.add_url_rule('/updatechannel', view_func=endpoints.update_channel, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)  # FIXME don't forget to remove debug=True later.
