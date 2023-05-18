from flask import Blueprint, render_template, request,flash

features = Blueprint("features", __name__)

# CAYMANN
@features.route("/ocr")
def ocr():
    return render_template("ocr.html")

# CAYMANN
@features.route("/conversion")
def conversion():
    return render_template("conversion.html")

# PUNEET
@features.route("/image-resizing")
def image_resizing():
    return render_template("imageResizing.html")

# PUNEET
@features.route("/image-compression")
def image_compression():
    return render_template("compression.html")

# PUNEET
@features.route("/image-coloring")
def image_coloring():
    return render_template("imageColoring.html")

# ! EXTRA FEATURES NOT NECCESSARY


@features.route("/text-to-image", methods=["GET", "POST"])
def text_to_image():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            print(prompt)
        else:
            flash("No prompt given !!!",category='error')

    return render_template("textToImage.html")


@features.route("/image-enhancement")
def image_enhancement():
    return render_template("imageEnhancement.html")
