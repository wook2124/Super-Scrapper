<!DOCTYPE html>
<html>
  <head>
  	<title>Job Search</title>
    <style>
      section {
        display: grid;
        gap: 20px;
        grid-template-columns: repeat(5, 1fr);
      }
    </style>
  </head>

  <body>
  	<h1>Search Results</h1>
    <h3>Found {{resultsNumber}} results for: {{searchingBy}}</h3>
    # a href로 export 추가함
    <a href="/export?word={{searchingBy}}" target="_blank">Export to CSV</a>
    <section>
      <h4>Title</h4>
      <h4>Company</h4>
      <h4>Location</h4>
      <h4>Salary</h4>
      <h4>Link</h4>
      {% for potato in jobs %}
        <span>{{potato.title}}</span>
        <span>{{potato.company}}</span>
        <span>{{potato.location}}</span>
        <span>{{potato.salary}}</span>
        <a href="{{potato.link}}" target="_blank">Apply</a>
      {% endfor %}
    </section>
  </body>
</html>


from flask import Flask, render_template, request, redirect
from scrapper import get_jobs


app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
  word = request.args.get('word')
  if word: 
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html", 
    searchingBy=word, 
    resultsNumber=len(jobs),
    jobs=jobs
  )

# export route를 추가함
@app.route("/export")
def export():
  # word를 쳤을 때(try)
  try:
    word = request.args.get('word')
    # word가 없다면
    if not word: 
      # except를 raise(일으킴)
      raise Exception()
    # word가 있다면 그대로 lower과 db에 저장함
    word = word.lower()
    jobs = db.get(word)
    # word가 db에 없다면
    if not jobs:
      # 마찬가지로 except를 raise(일으킴)
      raise Exception()
    return f"Generate CSV for {word}"
  # try에서 Error가 발생하면 처음 홈페이지로 redirect시킴
  except:
    return redirect("/")


app.run(host="0.0.0.0")
