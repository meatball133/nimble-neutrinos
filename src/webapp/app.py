from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    """Renders home page"""
    return render_template("index.html")

@app.route("/modify/<int:post_id>")
def modify(post_id: int):
    """Renders modify post page
    
    Still needs to be implemented
    """
    return f"Modifying post with post_id: {post_id}"

if __name__ == "__main__":
    app.run(debug=True)