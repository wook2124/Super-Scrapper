from flask import Flask, render_template, request, redirect
from scrapper import get_jobs


app = Flask("SuperScrapper")
# Fake data base를 빈 상태인 dictionary로 만듦
db = {}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
  word = request.args.get('word')
  if word: 
    word = word.lower()

    # fromdb를 만들어서 word에서 가져오는 것을 저장함
    fromdb = db.get(word)

    # word(단어)의 내용이 fromdb에 있으면 scrapping하지 않음
    if fromdb:
      jobs = fromdb
    
    # 없다면 get_jobs함수로 word에 해당하는 jobs을 가져온 뒤 db에 저장함
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")

  # resultsNumber로 가져온 jobs의 수(길이 len)을 보여줌
  return render_template("report.html", searchingBy=word, resultsNumber=len(jobs))


app.run(host="0.0.0.0")


<!DOCTYPE html>
<html>
  <head>
  	<title>Job Search</title>
  </head>

  <body>
  	<h1>Search Results</h1>
    <h3>Found {{resultsNumber}} results for: {{searchingBy}}</h3>
  </body>
</html>