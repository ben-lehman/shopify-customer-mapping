from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from app.helpers.api import Orders

import requests

bp = Blueprint('address', __name__)

@bp.route('/api/orders', methods=('GET',))
def orders():
    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations

    order_coords = order.get_coordinates()

    return jsonify(order_locations)

@bp.route('/map', methods=('GET',))
def map():


    return render_template('orders/locations.html')