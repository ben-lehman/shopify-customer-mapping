from app.helpers.api import Orders
from app import models
from app import db
from app.helpers.script import script

import click
import re
import zipcodes
import json
import requests

from app import create_app, db, migrate
from app.models import Customer


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Customer=Customer)

@app.cli.command()
def update_loc():
    num_rows = db.session.query(Customer).delete()
    db.session.commit()
    print("UPDATING!")

    order = Orders()
    order.set_order_count()
    order_count = order.count

    order.set_order_locations()
    order_locations = order.order_locations

    for location in order_locations:
        zcode = location['zip']
        customer = get_or_increase_zipcode(zcode)
        if customer is not None:
            db.session.add(customer)
            db.session.commit()
