from . import mainBP
from flask import render_template, request, redirect, url_for, make_response, send_from_directory, abort, current_app
import os



@mainBP.route("/", methods=["GET", "POST"])
def index():
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
    return render_template("index.html")