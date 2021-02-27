import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")
url = "https://www.iban.com/currency-codes"
get_url = requests.get(url)
get_url_soup = BeautifulSoup(get_url.text, "html.parser")
get_information = get_url_soup.find(
    "table", {"class": "table table-bordered downloads tablesorter"})
get_information = get_information.tbody
get_information_tr = get_information.find_all("tr")


def select_country(country_dic):
    try:
        user_number = int(input("#:"))
        if user_number in country_dic.keys():
            answer = country_dic[user_number]
            answer_code = answer[2]
            print(f"{answer[1]}")
            return answer_code
        else:
            print("Choose a number from the list")
            return select_country(country_dic)
    except:
        print("That wasn't a number.")
        return select_country(country_dic)


def exchange(currency_code_from, currency_code_to):
    try:
        print(
            f"How many {currency_code_from} do you want to convert to {currency_code_to}")
        user_amount = int(input(""))
        try:
            ex_url = f"https://transferwise.com/gb/currency-converter/{currency_code_from}-to-{currency_code_to}-rate?amount={user_amount}"
            ex_get_url = requests.get(ex_url)
            ex_get_url_soup = BeautifulSoup(ex_get_url.text, "html.parser")
            get_convert = ex_get_url_soup.find(
                "span", {"class": "text-success"})
            get_ex_rate = float(get_convert.string)
            currency_from = format_currency(user_amount, currency_code_from)
            currency_to = format_currency(
                user_amount*get_ex_rate, currency_code_to)
            print(f"{currency_from} is {currency_to}")
        except:
            print("Sorry We can't service")
    except:
        print("That's wasn't a number.")
        return exchange(currency_code_from, currency_code_to)


country_dic = {}
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


print("Where are you from? Choose a country by number.")
currency_code_from = select_country(country_dic)
print("Now choose another country.")
currency_code_to = select_country(country_dic)
exchange(currency_code_from, currency_code_to)
