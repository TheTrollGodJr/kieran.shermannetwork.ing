from flask import Flask, render_template, request, redirect, url_for

from pictureTime.routes import mainBP

from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials.env"))

PATH = __file__.rsplit("\\", 1)[0].replace("\\", "/")
app.config["FILES_DIRECTORY"] = f"{PATH}/static"

@app.route("/")
def index():
    userAgent = request.headers.get("User-Agent")
    if "Mobi" in userAgent: return render_template("index-mobile.html")
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

@app.route("/resume")
def resume():
    return render_template("resume.html")

##
##   todo: format this page to look better for desktop viewers
##
@app.route("/access-denied")
def denied():
    return render_template("access-denied.html")

##
##   todo: format this page to look better for desktop viewers
##
@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    host = os.getenv("HOST")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT"))

    app.config["API_KEY"] = os.getenv("API_KEY")

    app.register_blueprint(mainBP)

    app.run(host=host, debug=debug, port=port)#, ssl_context='adhoc')