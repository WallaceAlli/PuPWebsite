from flask import Flask
app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1> Pick Up Pal </h1>"

if __name__ == "__main__":
    app.run(debug=True)