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