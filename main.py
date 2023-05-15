from flask import Flask,render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
db = PyMongo(app).db

@app.route("/")
def home():
    # db.inventory.insert_one({"c":2})
    # a = db.inventory.find({})
    # for item in a:
        # print(item)
    # return f"<p>Hello World</p>"
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/services")
def services():
    return render_template("services.html")

if __name__ == '__main__':
    app.run(debug=True)