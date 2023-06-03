from flask import Flask, render_template
from flask import Blueprint

views = Blueprint("views", __name__)


@views.route("/")
def home():
    services = [
        {
            "title": "OCR",
            "description": "Transform image text into editable format with OCR."
        },
        {
            "title": "Image Coloring",
            "description": "Add colors to black and white or grayscale images."
        },
        {
            "title": "Image Compression",
            "description": "Reduce file size of images while maintaining quality."
        },
        {          
            "title": "Remove Background",
            "description": "Effortlessly remove backgrounds from images."
        }
    ]
    # db.inventory.insert_one({"c":2})
    # a = db.inventory.find({})
    # for item in a:
    # print(item)
    # return f"<p>Hello World</p>"
    return render_template("home.html", services=services)


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/contact")
def contact():
    return render_template("contact.html")


@views.route("/services")
def services():
    services = [
        {
            "title": "OCR",
            "description": "Convert image text into machine-readable format.",
            "link": "/services/ocr"
        },
        {
            "title": "Image Resizing",
            "description": "Crop and resize images to desired dimensions.",
            "link": "/services/image-resizing"
        },
        {
            "title": "Image Conversion",
            "description": "Reduce file size of images while maintaining quality.",
            "link": "/services/conversion"
        },
        {
            "title": "Image Compression",
            "description": "Reduce image file size without compromising quality.",
            "link": "/services/image-compression"
        },
        {
            "title": "Image Coloring",
            "description": "Enhance your images by adding vibrant colors and transforming",
            "link": "/services/image-coloring"
        },
        {
            "title": "Image to PDF",
            "description": "Converts images to PDF format, allowing you to create PDF.",
            "link": "/services/image-to-pdf"
        },
        {
            "title": "Image Enhancement",
            "description": "Enhance the quality and appearance of images.",
            "link": "/services/image-enhancement"
        },
        {
            "title": "Remove Background",
            "description": "Effortlessly remove image backgrounds.",
            "link": "/services/remove-background"
        }
    ]
    return render_template("services.html", services=services)
