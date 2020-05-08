from flask import Flask, render_template, request, redirect
# 전에 scrapping 해놨던 indeed.py를 가지고옴
# 그 중 get_jobs 함수를 사용할 것임
from scrapper import get_jobs


app = Flask("SuperScrapper")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
  word = request.args.get('word')
  if word: 
    # 검색하는 word(단어)를 lower(소문자)로만 출력함
    word = word.lower()
    # jobs를 word('recat, python...')친 것으로 검색함
    jobs = get_jobs(word)
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word)


app.run(host="0.0.0.0")



import requests
from bs4 import BeautifulSoup

# URL을 없애고 url로 argument를 설정함
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
      salary = None

    return {
        "title":
        title,
        "company":
        company,
        "location":
        location,
        "link":
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}",
        "salary":
        salary
    }

# url argument를 추가하고 default 값인 10으로 page를 검색함
def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{url}&start={page*50}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

# word argument를 추가하고 {}에 word argument로 검색할 수 있게함
# 다음으로 url argument도 추가해서 url 안에서 scrapping함
def get_jobs(word):
  url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}&limit=50"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs


# stackoverflow scrapper로 바꿈
import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company, location = html.find("h3").find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\r").strip("\n")
    job_id = html['data-jobid']
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Page: {page}")
        result = requests.get(f"{url}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
