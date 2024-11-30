from flask import Flask, render_template, request, redirect, url_for

from pictureTime.routes import mainBP

from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials.env"))

PATH = __file__.rsplit("\\", 1)[0].replace("\\", "/")
UPLOAD_FOLDER = PATH + "pictureTime/data/tempfiles"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}
app.config["FILES_DIRECTORY"] = f"{PATH}/static"
app.config["PROTECTED_PAGES"] = {"upload", "submitted"}
app.config["MOBILE_ONLY_PAGES"] = {"upload", "submitted", "login"}

@app.before_request
def checkAuthentication():
    #if request.endpoint == "denied": return None
    endpoint = request.endpoint

    if "." in endpoint:
        if endpoint.split(".")[-1] not in app.config["PROTECTED_PAGES"]: return
    elif endpoint not in app.config["PROTECTED_PAGES"]: return

    userAgent = request.headers.get("User-Agent")
    if "Mobi" not in userAgent: return redirect(url_for("denied"))

    # Skip login page so it doesn't redirect to itself
    #if request.endpoint == 'login':
    #    return None

    # Check if the 'auth' cookie is present and valid
    authCookie = request.cookies.get('auth')
    if authCookie != 'authorized':
        # Redirect to login if not authenticated
        return redirect(url_for('login'))

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
    host = os.getenv("HOST")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT"))

    app.register_blueprint(mainBP)

    app.run(host=host, debug=debug, port=port)