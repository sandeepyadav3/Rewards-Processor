"""
Building an API service with REST protocols to determine the reward points earned for each bill
PLEASE CHECK the READ.ME file for instructions to setup the environment in order to run this python-flask service
"""
from flask import Flask, json, request
import math

receipt_points_records = dict()

api = Flask(__name__)


@api.route('/receipts/process/', methods=['POST'])
def post_companies():
    content = request.json
    return calculate_total_points(content)


@api.route('/receipts/<rid>/points', methods=['GET'])
def get_points(rid):
    receipt_id = int(rid)
    if receipt_id in receipt_points_records.keys():
        return json.dumps({"points": receipt_points_records[receipt_id]}), 201
    else:
        return json.dumps({"Warning": "Receipt was not found. Please try again!"}), 201


def calculate_total_points(retailer_obj):
    retailer_points = points_from_retailer_name(retailer_obj['retailer'])
    bill_amount_points = points_from_total_bill(float(retailer_obj['total']))
    items_points = points_from_items(retailer_obj['items'])
    purchase_day_points = points_from_day_of_purchase(retailer_obj['purchaseDate'])
    purchase_time_points = points_from_time_of_purchase(retailer_obj['purchaseTime'])
    total_points = retailer_points + bill_amount_points + items_points + purchase_day_points + purchase_time_points
    new_id = len(receipt_points_records) + 1
    receipt_points_records[new_id] = total_points
    return {"receiptID": new_id,"points": total_points}


def points_from_retailer_name(name):
    points = 0
    for letter in name:
        if letter.isalpha() or letter.isnumeric():
            points += 1
    return points


def points_from_total_bill(total):
    points = 0
    if total.is_integer():
        points += 50
    if total % 0.25 == 0.00:
        points += 25
    return points


def points_from_items(items):
    points = 0
    eligible_items = int(len(items) / 2)
    points += (eligible_items * 5)
    for item in items:
        length = len(item['shortDescription'].strip())
        if length % 3 == 0:
            item_price = float(item['price']) * 0.2
            points += math.ceil(item_price)
    return points


def points_from_day_of_purchase(date):
    points = 0
    day_of_purchase = int(date[-2:])
    print(day_of_purchase % 2)
    if day_of_purchase % 2 == 1:
        points += 6
    return points


def points_from_time_of_purchase(time):
    points = 0
    hours = int(time[:2])
    minutes = int(time[-2:])
    if 14 <= hours <= 15 or (hours == 16 and minutes == 0):
        points += 10
    return points


if __name__ == '__main__':
    api.run()
