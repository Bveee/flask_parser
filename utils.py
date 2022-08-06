import time
from datetime import datetime

import requests
from flask import request
from psycopg2 import Error

from app_main import db
from models import ItemWB
from settings import CATALOG_URL, ROWS_PER_PAGE


def get_page(url):
    try:
        html_json = requests.get(url).json().get('data', {}).get('products')
    except:
        print("Error with URL!")
    return html_json


def json_to_dict(url):
    response_dict = get_page(url)
    response_uniq = dict()
    for key in range(len(response_dict)):
        response_uniq[response_dict[key]["id"]] = {
            "name": response_dict[key]["name"],
            "brand": response_dict[key]["brand"],
            "sale_price": response_dict[key]["salePriceU"]/100,
            "rating": response_dict[key]["rating"],
            "link": "https://www.wildberries.ru/catalog/{}/detail.aspx".format(
                response_dict[key]["id"]
            ),
        }
    return response_uniq


def update_db(page):
    response_dict = {1}
    timestamp = int(time.time())
    while len(response_dict) != 0:
        ids = {x.id for x in ItemWB.query.all()}
        response_dict = json_to_dict(CATALOG_URL+"&page={}".format(page))
        for key in response_dict:
            if key not in ids:
                item = ItemWB(
                    id=key,
                    name=response_dict[key]["name"],
                    brand=response_dict[key]["brand"],
                    sale_price=response_dict[key]["sale_price"],
                    rating=response_dict[key]["rating"],
                    link=response_dict[key]["link"],
                    history={timestamp: response_dict[key]["sale_price"]},
                )
                try:
                    db.session.add(item)
                    db.session.commit()
                except Error as e:
                    print(e)
                    print("Error, not add items DB.")
            else:
                item = dict(
                    db.session.query(ItemWB.history)
                    .filter(ItemWB.id == key).first()["history"]
                )
                item[timestamp] = response_dict[key]["sale_price"]
                ItemWB.query.filter_by(id=key).update(
                    dict(
                        sale_price=response_dict[key]["sale_price"],
                        history=item
                    )
                )
                try:
                    db.session.commit()
                    print(key, "Update price")
                except Error as e:
                    print(e)
                    print("Error, not update DB.")
        page += 1
        time.sleep(5)
    return "DB update!"


def view_db(page):
    page = request.args.get('page', page, type=int)
    my_list = ItemWB.query.order_by(ItemWB.rating.desc()) \
        .paginate(page=page, per_page=ROWS_PER_PAGE)
    return my_list


def history_id(id):
    date_list = dict(
        db.session.query(ItemWB.history)
        .filter(ItemWB.id == id).first()["history"]
    )
    my_list = dict()
    for key, value in date_list.items():
        dkey = datetime.utcfromtimestamp(int(key)).strftime(r'%d-%m-%Y %H:%M')    
        my_list[str(dkey)] = value
    return my_list
