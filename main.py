from flask import Flask,render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
db = PyMongo(app).db

@app.route("/")
def home_page():
    db.inventory.insert_one({"c":2})
    a = db.inventory.find({})
    for item in a:
        print(item)
    return f"<p>Helllo World</p>"

@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)