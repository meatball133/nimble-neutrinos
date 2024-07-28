from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    """Renders home page"""
    return render_template("index.html")

@app.route("/gallery")
def gallery():
    """Renders gallery page"""
    return render_template("gallery.html")

@app.route("/management")
def management():
    """Renders management page
    """
    return render_template("management.html")

if __name__ == "__main__":
    app.run(debug=True)