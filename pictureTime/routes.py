from . import mainBP
from flask import render_template, request, redirect, url_for, make_response, send_from_directory, abort, current_app, jsonify
from werkzeug.utils import secure_filename
import os
from .imgProcessing import processImg
from .encryption import checkPassword, loadUser
import json

def allowedFiles(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

@mainBP.route("/")
def pictureIndex():
    return render_template("pictureTime/index.html")

@mainBP.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            print("File not found")
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            print("No file name")
            return redirect(request.url)
        
        if file and allowedFiles(file.filename):
            print("File is allowed")
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            print("Saving image")
            file.save(filepath)
            print("Image saved\nProcessing image")
            processImg(filepath)
            print("Image processed")

            return redirect(url_for("main.submitted"))
    return render_template("pictureTime/upload.html")


@mainBP.route("/submitted")
def submitted():
    return render_template("pictureTime/submitted.html")

@mainBP.route("/logout")
def logout():
    resp = make_response(redirect(url_for("main.login")))
    resp.set_cookie('auth', '', expires=0)
    return resp

@mainBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = loadUser()
        for user in user_data:
            if user == username and checkPassword(password, user_data[user]):
                resp = make_response(redirect(url_for("main.upload")))
                resp.set_cookie('auth', 'authorized', max_age=60*60*24*365)
                return resp
    return render_template('pictureTime/login.html')

##
##      MAKE SURE THE VIDEO LOOKS GOOD ON MOBILE AND DESKTOP
##

@mainBP.route("/video")
def video():
    return render_template("pictureTime/video.html")

##
##   todo: add a create users page -- need to login for this; need admin code?
##
@mainBP.route("/add-user")
def addUser():
    return "WIP"

@mainBP.route("/status")
def status():
    try:
        with open(f"{current_app.config['DATA_FOLDER']}/status.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return f"Error: {e}"