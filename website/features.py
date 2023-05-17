from flask import Blueprint

features = Blueprint("features", __name__)

# CAYMANN
@features.route("/ocr")
def ocr():
    return "OCR"

# CAYMANN
@features.route("/conversion")
def conversion():
    return "Conversion"

# PUNEET
@features.route("/image-resizing")
def image_resizing():
    return "Image Resizing"

# PUNEET
@features.route("/image-compression")
def image_compression():
    return "Image Compression"

# PUNEET
@features.route("/image-coloring")
def image_coloring():
    return "Image Coloring"

# ! EXTRA FEATURES NOT NECCESSARY
@features.route("/text-to-image")
def text_to_image():
    return "Text to Image"


@features.route("/image-enhancement")
def image_enhancement():
    return "Image Enhancement"
