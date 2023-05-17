from flask import Flask, render_template
from flask import Blueprint

views = Blueprint("views", __name__)


@views.route("/")
def home():
    # db.inventory.insert_one({"c":2})
    # a = db.inventory.find({})
    # for item in a:
    # print(item)
    # return f"<p>Hello World</p>"
    return render_template("home.html")


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/contact")
def contact():
    return render_template("contact.html")


@views.route("/services")
def services():
    return render_template("services.html")
