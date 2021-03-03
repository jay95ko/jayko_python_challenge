import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"


def extract_dict(dic_in_list):
    return{
        "title": dic_in_list["title"],
        "url": dic_in_list["url"],
        "author": dic_in_list["author"],
        "points": dic_in_list["points"],
        "num_comments": dic_in_list["num_comments"],
        "objectID": dic_in_list["objectID"]
    }


def extract_data(url):
    requested_data = requests.get(url)
    data = requested_data.json()
    list_data = data["hits"]
    many = 0
    url_lists = []
    for dic_in_list in list_data:
        url_list = extract_dict(dic_in_list)
        url_lists.append(url_list)
        many = many + 1
        if many is 20:
            break
    return url_lists


def make_detail_url(id):
    print(f"{base_url}/items/{id}")
    return f"{base_url}/items/{id}"


def detail_extract_dict(dic_in_list):
    return{
        "title": dic_in_list["title"],
        "url": dic_in_list["url"],
        "author": dic_in_list["author"],
        "points": dic_in_list["points"]
    }


def detail_comment_extract_dict(dic_in_list):
    return{
        "title": dic_in_list["text"],
        "author": dic_in_list["author"],
    }


def detail_extract_data(data):
    children_data_list = data["children"]
    children_data_lists = []
    for children_data in children_data_list:
        children_datas = detail_comment_extract_dict(children_data)
        children_data_lists.append(children_datas)
    return children_data_lists


app = Flask("jayko")

db = {}


@app.route("/")
def home():
    data_list = []
    order = request.args.get('order_by')
    if order == 'new':
        pass
    else:
        order = 'popular'
    fromDb = db.get(order)
    if fromDb:
        pass
    else:
        if order == 'new':
            new = f"{base_url}/search_by_date?tags=story"
            new_lists = extract_data(new)
            db[order] = new_lists
            fromDb = db[order]
        else:
            popular = f"{base_url}/search?tags=story"
            popular_lists = extract_data(popular)
            db[order] = popular_lists
            fromDb = db[order]
    return render_template("index.html", lists=fromDb, order=order)


@app.route("/<id>")
def detail(id):
    url = make_detail_url(id)
    requested_data = requests.get(url)
    data = requested_data.json()
    children_data_lists = detail_extract_data(data)
    title_lists = detail_extract_dict(data)
    return render_template("detail.html", title_lists=title_lists, children_data_lists=children_data_lists)


app.run(host="0.0.0.0")
