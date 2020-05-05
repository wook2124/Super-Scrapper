from flask import Flask, render_template


app = Flask("SuperScrapper")

## @는 바로 밑에 있는 함수를 실행시킴
## 그리고 reunder_template는 awesome해서 
## 알아서 templates 폴더 안에 있는 home.html을 찾음
@app.route("/")
def home():
    return render_template("home.html")

## username이라는 argument가 와야 error가 안남
@app.route("/<username>")
def blahblah(username):
    return f"Hello, your name is {username}"


app.run(host="0.0.0.0")


## home.html
<!DOCTYPE html>
<html>
  <head>
  	<title>Job Search</title>
  </head>

  <body>
  	<h1>Job Search</h1>
    <form>
      <input placeholder='Search for a job' required />
      <button>Search</button>
    </form>
  </body>
</html>
