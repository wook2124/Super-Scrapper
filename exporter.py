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