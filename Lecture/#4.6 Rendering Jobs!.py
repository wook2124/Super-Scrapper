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
    
    # jobs를 가져와서 jobs로 다시 저장함
    jobs=jobs
  )


app.run(host="0.0.0.0")



<!DOCTYPE html>
<html>
  <head>
  	<title>Job Search</title>
    # html에서 section을 만들어 table을 생성함
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
    # 위에서 만든 section에 h4와 span으로 rendering(표현)함
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