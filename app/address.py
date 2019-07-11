from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_cors import cross_origin
from app.helpers.api import Orders
from app.models import db
from app.models import Customer

import requests

bp = Blueprint('address', __name__)


@bp.route('/update', methods=('GET', 'POST'))
def update():
    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations
    print(type(order_locations))

    for location in order_locations:
        customer = Customer(name=location['name'],
                            lat=location['latitude'],
                            lng=location['longitude'],
                            address1=location['address1'])
        db.session.add(customer)
        db.session.commit()

    flash('Locations have been updated')
    return render_template('orders/update.html')


@bp.route('/api/orders', methods=('GET',))
@cross_origin()
def orders():
    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations

    return jsonify(order_locations)

@bp.route('/map', methods=('GET',))
def map():
    return render_template('orders/locations.html')