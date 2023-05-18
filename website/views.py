from flask import Flask, render_template
from flask import Blueprint

views = Blueprint("views", __name__)


@views.route("/")
def home():
    services = [
        {
            "title": "OCR",
            "description": "Convert an image of text into machine-readable text format."
        },
        {
            "title": "Crop Images",
            "description": "Crop and resize your images to the desired dimensions."
        },
        {
            "title": "Apply Filters",
            "description": "Convert an image of text into machine-readable text format"
        },
        {
            "title": "Add Text",
            "description": "Insert text and captions to personalize your images."
        },
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
            "description": "Convert an image of text into machine-readable text format.",
            "link": "/services/ocr"
        },
        {
            "title": "Image Resizing",
            "description": "Crop and resize your images to the desired dimensions.",
            "link": "services/image-resizing"
        },
        {
            "title": "Image Conversion",
            "description": "Convert an image of text into machine-readable text format",
            "link": "services/conversion"
        },
        {
            "title": "Image Compression",
            "description": "Insert text and captions to personalize your images.",
            "link": "services/image-compression"
        },
        {
            "title": "Image Coloring",
            "description": "Convert an image of text into machine-readable text format",
            "link": "services/image-coloring"
        },
        {"title": "Text to Image",
            "description": "Crop and resize your images to the desired dimensions.",
            "link": "services/text-to-image"
         },
        {
            "title": "Image Enhancement",
            "description": "Insert text and captions to personalize your images.",
            "link": "services/image-enhancement"
        }
    ]
    return render_template("services.html", services=services)
