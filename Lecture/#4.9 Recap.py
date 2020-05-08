# flask에서 Flask와 render_template(표현하는 것), request, redirect, send file을 가져옴
from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_file

app = Flask("SuperScrapper")

db = {}

# home.html을 render_template으로 표현해서 "/" 첫 화면으로 사용함
@app.route("/")
def home():
    return render_template("home.html")

# home.html에서 required name으로 "word"를 이용해서 word를 argument로 사용함
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
  # home.html과 마찬가지로 report.html을 render_template으로 표현하고
  # report.html에서 사용할 각각의 argument를 설정함
  return render_template(
    "report.html", 
    searchingBy=word, 
    resultsNumber=len(jobs),
    job_result=jobs
  )

# report.html에서 만든 a href export를 설정함
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
    # csv 파일로 저장하는 기능을 사용함
    # 하지만 저장하는 파일의 이름에 대해서는 수정이 필요함
    save_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")


app.run(host="0.0.0.0")

# 파일 저장하는 부분을 수정했지만 실패
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
    save_file(jobs)
    file_name = f"static/results/file_path.csv"
    return send_file(file_name, mimetype='text/csv', attachment_filename=f'{word}_jobs.csv', as_attachment=True)    
  except:
    return redirect("/")


# home.html
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


# report.html
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
    <a href="/export?word={{searchingBy}}" target="_blank">Export to CSV</a>
    <section>
      <h4>Title</h4>
      <h4>Company</h4>
      <h4>Location</h4>
      <h4>Salary</h4>
      <h4>Link</h4>
      {% for potato in job_result %}
        <span>{{potato.title}}</span>
        <span>{{potato.company}}</span>
        <span>{{potato.location}}</span>
        <span>{{potato.salary}}</span>
        <a href="{{potato.link}}" target="_blank">Apply</a>
      {% endfor %}
    </section>
  </body>
</html>


# scrapper.py
import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")

    pages = []

    for link in links[0:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(whatever):
    title = whatever.find("h2", {"class": "title"}).find("a")["title"]

    company = whatever.find("span", {"class": "company"})
    if company is not None:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
      company = None

    location = whatever.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    job_id = whatever["data-jk"]

    salary = whatever.find("span", {"class": "salaryText"})
    if salary is not None:
        salary_anchor = salary.find("a")
        if salary_anchor is not None:
            salary = str(salary_anchor.string)
        else:
            salary = str(salary.string)
        salary = salary.strip()
    else:
      salary = ""

    return {
        "title":
        title,
        "company":
        company,
        "location":
        location,
        "salary":
        salary,
        "link":
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Page: {page}")
        result = requests.get(f"{url}&start={page*50}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
  url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}&limit=50"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs


# exporter.py
import csv

def save_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Location", "Salary", "Link"])
  # jobs에 있는 각 job을 가지고 row(행)를 작성함
  # job이 가진 값(value)의 list를 row(행)로 저장할 것임
  for job in jobs:
    writer.writerow(list(job.values()))
  return