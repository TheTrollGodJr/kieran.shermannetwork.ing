from flask import Flask, render_template
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials.env"))

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    host = os.getenv("HOST")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT"))

    app.run(host=host, debug=debug, port=port)