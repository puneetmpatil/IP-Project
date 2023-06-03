from werkzeug.utils import secure_filename
import os
from .utility import allowed_file,OCR_Function, compress_image,enhance_image, remove_bg, imageToPDF, resizing,coloring,convertFormat
from flask import Blueprint, render_template, request, flash, redirect, url_for
features = Blueprint("features", __name__)

UPLOAD_FOLDER = "website/uploads"

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
            filename=OCR_Function(filename)
            #return redirect(url_for('features.ocr', filename=filename))

            flash(f"Your text has been processed and is available at <a href='/static/{filename}' target='_blank' class='text-red-500 underline'>here</a>", category="success")

            return redirect(url_for('features.ocr', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("ocr.html")

# ! DONE
@features.route("/conversion", methods=['GET', 'POST'])
def conversion():
    if request.method == "POST":
        operation = request.form.get('operation')
        if operation == 'Choose a option':
            flash("Please choose an option", category="error")
            return redirect(request.url)
        
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        
        if operation == file.filename.split(".")[1].lower():
            flash("Please choose a different format", category="error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/conversion/{filename}")
            flash("File uploaded successfully", category="success")

            # Perform conversion
            newFileName = convertFormat(filename,operation)
            flash(f"Your image has been processed and is available at <a href='/static/{newFileName}' target='_blank' class='text-red-500 underline'>here</a>", category="success")

            return redirect(url_for('features.conversion', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("conversion.html")

# ! DONE
@features.route("/image-resizing", methods=['GET', 'POST'])
def image_resizing():
    if request.method == "POST":
        width = request.form.get('width')
        height = request.form.get('height')
        if not width:
            flash("Please provide a width")
        elif not width.isnumeric():
            flash("Please provide a valid width")
        if not height:
            height = width
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
            height = int(height)
            width = int(width)
            new_filename = resizing(filename = filename,height=height,width=width)
            flash(f"Your image has been processed and is available at <a href='/static/{new_filename}' target='_blank' class='text-red-500 underline'>here</a>", category="success")

            return redirect(url_for('features.image_resizing', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("imageResizing.html")

# ! DONE
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
            flash(f"Your image has been processed and is available at <a href='/static/{newFileName}' target='_blank' class='text-red-500 underline'>here</a>", category="success")


            return redirect(url_for('features.image_compression', filename=filename))
        else:
            flash("Invalid file format", category="error")

    return render_template("compression.html")

# ! DONE
@features.route("/image-coloring", methods=['GET', 'POST'])
def image_coloring():
    if request.method == "POST":
        operation = request.form.get('operation')
        if operation == 'Choose a option':
            flash("Please choose an option", category="error")
            return redirect(request.url)
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
            newfilename = coloring(filename,operation)
            flash(f"Your image has been processed and is available at <a href='/static/{newfilename}' target='_blank' class='text-red-500 underline'>here</a>", category="success")

            return redirect(url_for('features.image_coloring', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("imageColoring.html")

# ! EXTRA FEATURES NOT NECCESSARY
@features.route("/image-to-pdf", methods=["GET", "POST"])
def image_to_pdf():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        files = request.files.getlist("file")
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if not files:
            flash('No selected file', category="error")
        
        filenames = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filenames.append(filename)
                file.save(f"{UPLOAD_FOLDER}/imageToPDF/{filename}")
            else:
                flash("Invalid file format", category="error")

        flash("File uploaded successfully", category="success")
            # Perform image compression
        print(filenames)
        newFileName = imageToPDF(filenames)
        flash(f"Your pdf is available at <a href='/static/{newFileName}' target='_blank' class='text-red-500 underline'>here</a>", category="success")


        return redirect(url_for('features.image_to_pdf'))

    return render_template("imageToPDF.html")


# ! DONE
@features.route("/image-enhancement", methods=['GET', 'POST'])
def image_enhancement():
    if request.method == "POST":
        operation = request.form.get('operation')
        if operation == 'Choose a option':
            flash("Please choose an option", category="error")
            return redirect(request.url)
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

            # Perform image enhancement
            newFileName = enhance_image(filename,operation)
            flash(f"Your image has been processed and is available at <a href='/static/{newFileName}' target='_blank' class='text-red-500 underline'>here</a>", category="success")


            return redirect(url_for('features.image_enhancement', filename=filename))
        else:
            flash("Invalid file format", category="error")
    return render_template("imageEnhancement.html")


# ! DONE
# ? Remove background from images
@features.route('/remove-background',methods=['POST','GET'])
def remove_background():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part", category="error")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/backgroundRemover/{filename}")
            flash("File uploaded successfully", category="success")

            # Remove background
            newFileName = remove_bg(filename)
            flash(f"Your image has been processed and is available at <a href='/static/{newFileName}' target='_blank' class='text-red-500 underline'>here</a>", category="success")

            return redirect(url_for('features.image_enhancement', filename=filename))
        else:
            flash("Invalid file format", category="error")
            

    return render_template("removeBackground.html")