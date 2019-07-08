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
                lon = shipping_address.get('longitude')
                lat = shipping_address.get('latitude')
                current_cords = {'longitude': lon, 'latitude': lat}

                if current_cords not in self.order_locations:
                    self.order_locations.append(current_cords)
            except:
                print("There wasn't any shipping address associated with this order")

        return

