from flask import Flask
import endpoints

app = Flask(__name__)

app.add_url_rule('/', view_func=endpoints.mainpage)
app.add_url_rule('/view', view_func=endpoints.gallery)

if __name__ == '__main__':
    app.run(debug=True)  # FIXME don't forget to remove debug=True later.
