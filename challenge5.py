import os
import csv
import requests
from bs4 import BeautifulSoup
# encoding='utf-8-sig'

os.system("clear")
alba_url = "http://www.alba.co.kr"

get_url = requests.get(alba_url)
get_url_soup = BeautifulSoup(get_url.text, "html.parser")
get_company = get_url_soup.find("div", {"id": "MainSuperBrand"}).find_all(
    "a", {"class": "brandHover"})

for company in get_company:
    link = company.attrs["href"]
    company_name = company.find(
        "span", {"class": "company"}).find("strong").string
    file = open(f"{company_name}.csv", mode="w",
                encoding='UTF-8-sig', newline="")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    url = f"{link}"
    get_company_url = requests.get(url)
    get_company_url_soup = BeautifulSoup(get_company_url.text, "html.parser")
    get_alba_component = get_company_url_soup.find(
        "div", {"id": "NormalInfo"}).find("tbody").find_all("tr")
    for component in get_alba_component:
        try:
            component_information = {
                "place": component.find("td", {"class": "local first"}).get_text().replace('\xa0', ' '),
                "title": component.find("span", {"class": "company"}).string,
                "time": component.find("span", {"class": "time"}).string,
                "pay": [component.find("span", {"class": "payIcon"}).string, component.find("span", {"class": "number"}).string],
                "date": component.find("td", {"class": "regDate last"}).string
            }
            writer.writerow(list(component_information.values()))
        except:
            i = 1
