from . import mainBP
from flask import render_template, request, redirect, url_for, make_response, send_from_directory, abort, current_app
import os

@mainBP.route("/")
def pictureIndex():
    return render_template("pictureTime/index.html")

@mainBP.route("/upload", methods=["GET", "POST"])
def upload():
    return "WIP"
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowedFiles(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            processImg(filepath)

            return redirect(url_for("submitted"))
    return render_template("pictureTime/upload.html")


@mainBP.route("/submitted")
def submitted():
    return render_template("pictureTime/submitted.html")

@mainBP.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie('auth', '', expires=0)
    return resp

@mainBP.route("/login")
def login():
    return render_template("pictureTime/login.html")

##
##      MAKE SURE THE VIDEO LOOKS GOOD ON MOBILE
##

@mainBP.route("/video")
def video():
    return render_template("pictureTime/video.html")