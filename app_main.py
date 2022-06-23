# import json
import os

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import ItemWB


def get_page(url):
    html_json = requests.get(url).json()['data']['products']
    return html_json


def get_ids():
    ids = set()
    results = ItemWB.query.all()
    for result in results:
        ids.add(result.id)
    return ids


def json_to_dict(url):
    html_json = get_page(url)
    response_uniq = dict()
    response_dict = html_json
    # print(response_dict)
    for key in range(len(response_dict)):
        # re.search(r'\d\d\d.*[x|х|\*].*\d\d\d', response_dict[key]["name"])
        response_uniq[response_dict[key]["id"]] = {
            "name": response_dict[key]["name"],
            "brand": response_dict[key]["brand"],
            "salePriceU": response_dict[key]["salePriceU"]/100,
            "rating": response_dict[key]["rating"],
            "link": "https://www.wildberries.ru/catalog/{}/detail.aspx".format(
                response_dict[key]["id"]
            ),
            }
    return response_uniq


@app.route('/')
def print_dict():
    url = "https://catalog.wb.ru/catalog/electronic3/catalog?locale=ru&" \
        "subject=515"
    response_dict = json_to_dict(url)
    return response_dict


@app.route('/new')
def save_dict():
    page = 30
    response_dict = {1}
    while len(response_dict) != 0:
        ids = get_ids()
        url = "https://catalog.wb.ru/catalog/electronic3/catalog?locale=ru&" \
            "subject=515&page={}".format(page)
        response_dict = json_to_dict(url)
        for key in response_dict:
            if key not in ids:
                item = ItemWB(
                    id=key,
                    name=response_dict[key]["name"],
                    brand=response_dict[key]["brand"],
                    salePriceU=response_dict[key]["salePriceU"],
                    rating=response_dict[key]["rating"],
                    link=response_dict[key]["link"],
                )
                db.session.add(item)
                db.session.commit()
            else:
                item = ItemWB.query.filter_by(id=key).update(
                    dict(salePriceU=response_dict[key]["salePriceU"])
                )
                db.session.commit()
                print(key, "update price")
        page += 1
        time.sleep(5)
    return ("Created!", page)


if __name__ == '__main__':
    app.run(debug=True)
