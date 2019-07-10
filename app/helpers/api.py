from flask import jsonify
import json
import requests

from config import Config


def get_response(shop, endpoint, params=''):
    if params == '':
        response = requests.get("%s%s" % (shop, endpoint))
    else:
        response = requests.get("%s%s&%s" % (shop, endpoint, params))

    return response

def post_script(shop, endpoint, file, params='':
    if params == '':
        response = requests.get("%s%s" % (shop, endpoint))
    else:
        response = requests.get("%s%s&%s" % (shop, endpoint, params))


class Orders:
    shop = Config.SHOPIFY_CONFIG['HOST']
    key = Config.SHOPIFY_CONFIG['API_KEY']
    sec = Config.SHOPIFY_CONFIG['API_SEC']
    api_version = Config.SHOPIFY_CONFIG['API_VERSION']

    def __init__(self, myshop=shop, mykey=key, mysec=sec, myapi=api_version):
        self.count = ""
        self.order_locations = []
        self.shop_url = "https://%s:%s@%s/admin/api/%s/" % (mykey, mysec, myshop, myapi)

    def set_order_count(self):
        order_endpoint = "orders/count.json?status=any"

        order_count_response = get_response(self.shop_url, order_endpoint)
        order_count = json.loads(order_count_response.content.decode('utf-8')).get('count')

        self.count = order_count
        return

    def set_order_locations(self):
        location_endpoint = 'orders.json?fields=shipping_address&status=any'

        location_response = get_response(self.shop_url, location_endpoint)
        all_locations = json.loads(location_response.content.decode('utf-8')).get('orders')

        for address in all_locations:
            try:
                shipping_address = address['shipping_address']
                self.order_locations.append(shipping_address)
            except:
                print("There wasn't any shipping address associated with this order")

        return

    def get_coordinates(self):
        all_coords = []

        for location in self.order_locations:
            lon = location['longitude']
            lat = location['latitude']

            current_coords = {'longitude': lon, 'latitude': lat}
            if current_coords not in all_coords:
                all_coords.append(current_coords)

        return all_coords


