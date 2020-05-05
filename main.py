from flask import Flask, render_template, request

app = Flask("SuperScrapper")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/<username>")
def blahblah(username):
    return f"Hello, your name is {username}"


@app.route("/report")
def report():
  word = request.args.get('word')
  return render_template("report.html", blahblue=word)


app.run(host="0.0.0.0")
