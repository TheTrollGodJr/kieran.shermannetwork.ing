from . import mainBP
from flask import render_template, request


@mainBP.route("/")
def pictureIndex():
    return render_template("pictureTime/index.html")

@mainBP.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template('pictureTime/login.html')


@mainBP.route("/submitted")
def submitted():
    return render_template("pictureTime/submitted.html")

@mainBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('pictureTime/login.html')

@mainBP.route("/video")
def video():
    return render_template("pictureTime/video.html")
