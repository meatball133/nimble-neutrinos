from flask import Flask
from src.webapp import endpoints
app = Flask(__name__)

app.add_url_rule('/', view_func=endpoints.mainpage)
app.add_url_rule('/view', view_func=endpoints.gallery)
app.add_url_rule('/manage', view_func=endpoints.management)

if __name__ == '__main__':
    app.run(debug=True)  # FIXME don't forget to remove debug=True later.
