from flask import Flask, render_template, request, redirect, url_for

from pictureTime.routes import mainBP

from dotenv import load_dotenv
import os

import json

app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials.env"))

PATH = __file__.rsplit("\\", 1)[0].replace("\\", "/")
UPLOAD_FOLDER = PATH + "/pictureTime/data/tempfiles"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DATA_FOLDER"] = f"{PATH}/pictureTime/data"
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}
app.config["FILES_DIRECTORY"] = f"{PATH}/static"
app.config["PROTECTED_PAGES"] = {"main.upload", "main.submitted"}
app.config["MOBILE_ONLY_PAGES"] = {"main.upload", "main.submitted", "main.login"}

def setupUsersJsonFile():
    if not os.path.exists(f"{app.config['DATA_FOLDER']}/users.json"):
        setup = {"username":"password", "username2":"password2"}
        with open(f"{app.config['DATA_FOLDER']}/users.json", "w") as f:
            json.dump(setup, f, indent=4)

    if not os.path.exists(f"{app.config['DATA_FOLDER']}/info.json"):
        setup = {"photo_number":0}
        with open(f"{app.config['DATA_FOLDER']}/info.json", "w") as f:
            json.dump(setup, f, indent=4)

@app.before_request
def checkAuthentication():
    #if request.endpoint == "denied": return None
    endpoint = request.endpoint
    #print(endpoint)

    userAgent = request.headers.get("User-Agent")
    #print(userAgent, type(userAgent))
    if "Mobi" not in userAgent and endpoint in app.config["MOBILE_ONLY_PAGES"]: return redirect(url_for("denied"))

    if endpoint not in app.config["PROTECTED_PAGES"]: return


    # Skip login page so it doesn't redirect to itself
    #if request.endpoint == 'login':
    #    return None

    # Check if the 'auth' cookie is present and valid
    authCookie = request.cookies.get('auth')
    if authCookie != 'authorized':
        # Redirect to login if not authenticated
        return redirect(url_for('main.login'))

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
    setupUsersJsonFile()

    host = os.getenv("HOST")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT"))

    app.register_blueprint(mainBP)

    app.run(host=host, debug=debug, port=port)