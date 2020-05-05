from flask import Flask, render_template

app = Flask("SuperScrapper")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/<username>")
def blahblah(username):
    return f"Hello, your name is {username}"


app.run(host="0.0.0.0")
