from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)

from app.helpers.api import Orders

import requests

bp = Blueprint('address', __name__)

@bp.route('/orders', methods=('GET',))
def orders():
    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations

    order_coords = order.get_coordinates()

    return render_template('orders/locations.html',
                           count=order_count,
                           locations=order_locations,
                           coords=order_coords)