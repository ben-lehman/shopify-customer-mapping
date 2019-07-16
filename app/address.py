from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_cors import cross_origin
from app.helpers.api import Orders
from app import models
from app import db

import json
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
        customer = models.Customer(lat=location['latitude'],
                                   lng=location['longitude'],
                                   zipcode=location['zip']
                            )
        models.db.session.add(customer)
        models.db.session.commit()

    flash('Locations have been updated')
    return render_template('orders/update.html')


@bp.route('/clear', methods=('Get',))
def clear():
    num_rows = models.db.session.query(models.Customer).delete()
    models.db.session.commit()

    return 'Deleted'


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