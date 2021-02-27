import requests
import os


def clear():
    os.system("clear")


def check_status(i):
    try:
        statu = requests.get(i)
        statu_code = statu.status_code
        statu_code == 200
        print(f"{i} is UP!")
    except:
        print(f"{i} is DOWN!")
    return


def check_over_fun():
    print("Do tou want start over? y/n")
    check_over = input()
    if check_over == "y":
        return check_over
    elif check_over == "n":
        return check_over
    else:
        check_over == "error"
        print("That's not a valid answer")
        return check_over


while True:
    print("Please write a URL or URLs you want to check. (separated by comma)")
    User_url = input()
    Separated_url = []
    Separated_url = User_url.split(",")
    check_over = ""
    for i in Separated_url:
        inspect_string = i.strip()
        if inspect_string.endswith('.com') is True:
            if inspect_string.startswith("http://") is True:
                check_status(inspect_string)
            else:
                inspect_string = "http://" + inspect_string
                check_status(inspect_string)
        else:
            print(f"{inspect_string} is not a valid URL")
    while True:
        a = check_over_fun()
        if a == "y":
            clear()
            break
        elif a == "n":
            check_over = "break"
            print("k. bye")
            break
    if check_over == "break":
        break
