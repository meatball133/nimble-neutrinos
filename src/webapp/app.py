from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    """Renders home page"""
    return render_template("index.html")

@app.route("/edit-tags/<int:post_id>")
def edit_tags(post_id: int):
    """Renders edit post tags page
    
    Still needs to be implemented
    """
    return f"Editing tags of post with post_id: {post_id}"

if __name__ == "__main__":
    app.run(debug=True)