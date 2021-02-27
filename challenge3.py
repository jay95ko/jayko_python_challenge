import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

get_url = requests.get(url)

get_url_soup = BeautifulSoup(get_url.text, "html.parser")

get_information = get_url_soup.find(
    "table", {"class": "table table-bordered downloads tablesorter"})

get_information = get_information.tbody

get_information_tr = get_information.find_all("tr")


def main(country_dic):
    try:
        user_number = int(input("#:"))
        for number in country_dic.keys():
            if number == user_number:
                answer = country_dic[number]
                print(f"You chose {answer[1]}")
                print(f"The currency code is {answer[2]}")
                return
        print("Choose a number from the list")
        main(country_dic)
    except:
        print("That wasn't a number.")
        main(country_dic)


country_dic = {}
print("Hello! Please choose select a country by number:")
country_number = 0
for tr in get_information_tr:
    tds = []
    tds.append(country_number)
    get_information_tds = tr.find_all("td")
    for td in get_information_tds:
        tds.append(td.string)
    if tds[3] != None:
        tds = tds[0], tds[1], tds[3]
        country_dic[tds[0]] = tds
        country_number += 1

for number in country_dic.keys():
    answer = country_dic[number]
    print(f"# {answer[0]} {answer[1]}")

main(country_dic)
