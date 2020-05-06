from flask import Flask, render_template, request

app = Flask("SuperScrapper")


@app.route("/")
def home():
    return render_template("home.html")


## form의 action으로 page가 넘어올 때
## placeholder로 입력한 word를 argument화해서
## report.html에 있는 blahblue로 넘겨줌
@app.route("/report")
def report():
  word = request.args.get('word')
  return render_template("report.html", blahblue=word)


app.run(host="0.0.0.0")


## form의 action으로 /report로 가는 것을 추가하고
## placholder로 입력하는 required name은 "word"로 함
<!DOCTYPE html>
<html>
  <head>
  	<title>Job Search</title>
  </head>

  <body>
  	<h1>Job Search</h1>
    <form action="/report" method="get">
      <input placeholder='Search for a job' required name="word" />
      <button>Search</button>
    </form>
  </body>
</html>


## {{blahblue}}를 통해 argument를 받아서 rendering(표현)함
<!DOCTYPE html>
<html>
  <head>
  	<title>Job Search</title>
  </head>

  <body>
  	<h1>Search Results</h1>
    <h3>You are looking for {{blahblue}}</h3>
  </body>
</html>