from flask import Flask

app = Flask("SuperScrapper")


@app.route("/")
def home():
    return "Hello! Welcome to mi casa!"


@app.route("/contact")
def blahblah():
    return "Contact me!"

## Repl.it이 알 수 있게끔 host="0.0.0.0"을 설정함
app.run(host="0.0.0.0")
