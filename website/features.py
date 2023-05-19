from werkzeug.utils import secure_filename
import os
from .utility import allowed_file, create_image,compress_image
from flask import Blueprint, render_template, request, flash, redirect, url_for
features = Blueprint("features", __name__)

UPLOAD_FOLDER = "website/static/uploads"

# CAYMANN


@features.route("/ocr", methods=['GET', 'POST'])
def ocr():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/ocr/{filename}")
            flash("File uploaded successfully", category="success")

            # Perform optical character recognition

            return redirect(url_for('features.ocr', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("ocr.html")

# CAYMANN
@features.route("/conversion", methods=['GET', 'POST'])
def conversion():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/conversion/{filename}")
            flash("File uploaded successfully", category="success")

            # Perform conversion


            return redirect(url_for('features.conversion', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("conversion.html")

# PUNEET
@features.route("/image-resizing", methods=['GET', 'POST'])
def image_resizing():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/resizing/{filename}")
            flash("File uploaded successfully", category="success")

            # Perform image resizing


            return redirect(url_for('features.image_resizing', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("imageResizing.html")

# PUNEET
@features.route("/image-compression", methods=['GET', 'POST'])
def image_compression():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash("File uploaded successfully", category="success")
            file.save(f"{UPLOAD_FOLDER}/compression/{filename}")

            # Perform image compression
            newFileName = compress_image(filename)
            flash(f"Your image has been processed and is available at <a href='/static/{newFileName}' target='_blank'>here</a>", category="success")


            return redirect(url_for('features.image_compression', filename=filename))
        else:
            flash("Invalid file format", category="error")

    return render_template("compression.html")

# PUNEET
@features.route("/image-coloring", methods=['GET', 'POST'])
def image_coloring():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/coloring/{filename}")
            flash("File uploaded successfully", category="success")

            # Perform image coloring


            return redirect(url_for('features.image_coloring', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("imageColoring.html")

# ! EXTRA FEATURES NOT NECCESSARY


@features.route("/text-to-image", methods=["GET", "POST"])
def text_to_image():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            create_image(prompt)
            # image.save(f"{prompt}.png")
        else:
            flash("No prompt given !!!", category='error')

    return render_template("textToImage.html")


@features.route("/image-enhancement", methods=['GET', 'POST'])
def image_enhancement():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/enhancement/{filename}")
            flash("File uploaded successfully", category="success")

            # Perform image compression


            return redirect(url_for('features.image_enhancement', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("imageEnhancement.html")
