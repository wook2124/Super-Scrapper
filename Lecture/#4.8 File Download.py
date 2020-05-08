from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
# csv 기능 가져옴
from exporter import save_file

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


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word: 
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    # 위의 내용들이 다 실행되고 나면 jobs db에 word가 저장됨
    # 그 상태에서 save_file을 실행해서 csv 파일을 만듦 
    save_file(jobs)
    # 하지만 저장할 때 파일이름이 "jobs.csv"가 아닌 export만 뜸
    # 수정 필요함
    return send_file("jobs.csv")
  except:
    return redirect("/")


app.run(host="0.0.0.0")
