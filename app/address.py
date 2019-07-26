from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_cors import cross_origin
from app.helpers.api import Orders
from app import models
from app import db
from app.helpers.script import script

import click
import re
import zipcodes
import json
import requests

bp = Blueprint('address', __name__)


def get_or_increase_zipcode(new_zipcode):
    zipcode = models.db.session.query(models.Customer).filter_by(zipcode=new_zipcode).first()
    if not zipcode:
        coords = get_coords_from_zipcode(new_zipcode)
        if coords:
            lat, lng = coords
            zipcode = models.Customer(lat, lng, new_zipcode)
        else:
            return
    else:
        zipcode.count += 1
    return zipcode


def get_coords_from_zipcode(zipcode):
    postal_code = re.search('\d{5}(-\d{4})?$', zipcode)
    if postal_code is not None:
        cur_zip = zipcodes.matching(zipcode)
        return (cur_zip[0]['lat'], cur_zip[0]['long'])
    return


@bp.route('/update', methods=('GET',))
def update():
    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations

    for location in order_locations:
        zcode = location['zip']
        customer = get_or_increase_zipcode(zcode)
        if customer is not None:
            models.db.session.add(customer)
            models.db.session.commit()

    flash('Locations have been updated')
    return render_template('orders/update.html')


@bp.route('/clear', methods=('Get',))
def clear():
    num_rows = models.db.session.query(models.Customer).delete()
    models.db.session.commit()

    return 'Deleted'

@bp.cli.command('update-all')
def update_all():
    num_rows = models.db.session.query(models.Customer).delete()
    models.db.session.commit()

    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations

    for location in order_locations:
        zcode = location['zip']
        customer = get_or_increase_zipcode(zcode)
        if customer is not None:
            models.db.session.add(customer)
            models.db.session.commit()

    return 'Updated'


@bp.route('/write', methods=('Get', 'PUT'))
def write():
    all_customers = models.Customer.query.all()
    data = []
    for c in all_customers:
        data.append(c.to_dict())

    json_data = json.dumps(data)
    js_data = "script = \"\"\"const data = " + json_data + "\n" + script + "\"\"\""

    f = open("app/gen/mymap.py", "w")
    f.write(js_data)
    f.close

    return js_data


@bp.route('/post', methods=('GET', 'PUT'))
def post():
    num_rows = models.db.session.query(models.Customer).delete()
    models.db.session.commit()

    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations

    for location in order_locations:
        zcode = location['zip']
        customer = get_or_increase_zipcode(zcode)
        if customer is not None:
            models.db.session.add(customer)
            models.db.session.commit()

    order.put_data()

    return "Success!"


@bp.route('/api/orders', methods=('GET',))
@cross_origin()
def orders():
    all_customers = models.Customer.query.all()
    data = []
    for c in all_customers:
        data.append(c.to_dict())

    return jsonify(data)


@bp.route('/map', methods=('GET',))
def map():
    return render_template('orders/locations.html')
