from . import mainBP
from flask import render_template, request, redirect, url_for, make_response, send_from_directory, current_app, jsonify, request
from werkzeug.utils import secure_filename
import os
from .imgProcessing import processImg, setInfoStatus
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
            #print("No file name")
            return redirect(request.url)
        
        if file and allowedFiles(file.filename):
            #print("File is allowed")
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config["FILES_DIRECTORY"], filename)
            #print("Saving image")
            file.save(filepath)
            #print("Image saved\nProcessing image")
            processImg(filepath)
            #print("Image processed")

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
        return jsonify(data), 200
    except Exception as e:
        return f"Error: {e}", 404
    
@mainBP.route("/<filename>")
def download(filename: str):
    try:
        if request.headers.get("X-API-KEY") == current_app.config["API_KEY"]:
            if os.path.exists(f"{current_app.config['FILES_DIRECTORY']}/{filename}") and filename != "":
                return send_from_directory(current_app.config['FILES_DIRECTORY'], filename, as_attachment=True), 200
            return "Not Found", 404
        return "Unauthorized", 401
    except:
        return "Bad Request", 400

@mainBP.route("/delete/<filename>")
def delete(filename: str):
    #print("ran delete")
    try:
        if request.headers.get("X-API-KEY") == current_app.config["API_KEY"]:
            print("KEY accepted")
            try:
                print(f"{current_app.config['FILES_DIRECTORY']}/{filename}")
                if os.path.exists(f"{current_app.config['FILES_DIRECTORY']}/{filename}") and filename != "":
                    os.remove(f"{current_app.config['FILES_DIRECTORY']}/{filename}")
                    if "processed" in filename: setInfoStatus("processed", filename, True)
                    else: setInfoStatus("original", filename, True)
                    return "Success", 200
            except Exception as e:
                print(f"Error deleting file: {e}")
                return "Not Found", 404
        return "Unauthorized", 401
    except Exception as e:
        print(e)
        return "Bad Request", 400

@mainBP.route("/upload-video", methods=['GET', 'POST'])
def uploadVideo():
    try:
        if request.headers.get("X-API-KEY") == current_app.config("API_KEY"):
            if 'file' not in request.files:
                return "Not Found", 404
            file = request.files['file']
            if file.filename == '':
                return "Not Found", 404
            elif "mp4" not in file.filename:
                return "Unsupported Media Type", 415
            
            #filename = secure_filename(file.filename)
            filepath = f"{current_app.config['FILES_DIRECTORY']}/video/out.mp4"
            if os.path.exists(filepath): os.remove(filepath)
            file.save(filepath)

    except Exception as e:
        print(e)
        return "Bad Request", 400