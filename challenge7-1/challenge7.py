import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""


subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")


def find_subject_content(subreddit):
    subreddit_list = []
    content = 0
    url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"
    get_url = requests.get(url, headers=headers)
    get_url_soup = BeautifulSoup(get_url.text, "html.parser")
    get_content_boxs = get_url_soup.find_all(
        "div", {"class": "_1poyrkZ7g36PawDueRza-J"})
    for get_content_box in get_content_boxs:
        if content == 1:
            pass
        else:
            get_sub = find_subject_content_sub(get_content_box, subreddit)
            subreddit_list.append(get_sub)
        content = content + 1
        if content == 7:
            return subreddit_list
    return subreddit_list


def find_subject_content_sub(get_content_box, subreddit):
    get_vote = get_content_box.find(
        "div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).string
    get_title = get_content_box.find(
        "h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).string
    subject = f"r/{subreddit}"
    get_url = get_content_box.find(
        "a", {"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})["href"]
    if get_vote.find("k") != -1:
        get_vote_trash = get_vote.replace("k", "")
        get_vote_int = float(get_vote_trash)*1000
    else:
        get_vote_int = int(get_vote)
    return{
        'vote': get_vote,
        'vote_int': get_vote_int,
        'title': get_title,
        'subject': subject,
        'url': get_url
    }


@app.route("/")
def home():
    return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():
    subreddits_Db = []
    answer_subject_Db = ""
    for subreddit in subreddits:
        answer_subject = request.args.get(f"{subreddit}")
        if answer_subject == "on":
            answer_subject_Db = answer_subject_Db + f"r/{subreddit}"
            get_subject_lists = find_subject_content(subreddit)
            for get_subject_list in get_subject_lists:
                subreddits_Db.append(get_subject_list)

    subreddits_Db = sorted(
        subreddits_Db, key=lambda x: x['vote_int'], reverse=True)
    return render_template("read.html", subreddits=subreddits, subreddits_Db=subreddits_Db, answer_subject_Db=answer_subject_Db)


app.run(host="0.0.0.0")
