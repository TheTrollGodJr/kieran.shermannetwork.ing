from flask import Flask, render_template

#from pictureTime.routes import mainBP

from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials.env"))

PATH = __file__.rsplit("\\", 1)[0].replace("\\", "/")
UPLOAD_FOLDER = PATH + "pictureTime/data/tempfiles"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}
app.config["FILES_DIRECTORY"] = f"{PATH}/static"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/coding")
def coding():
    return render_template("coding.html")

@app.route("/conlangs")
def conlangs():
    return render_template("conlangs.html")

@app.route("/photography")
def photography():
    return render_template("photography.html")

@app.route("/picture-time")
def pictureTime():
    return None

@app.route("/resume")
def resume():
    return render_template("resume.html")

if __name__ == "__main__":
    host = os.getenv("HOST")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT"))

    app.run(host=host, debug=debug, port=port)