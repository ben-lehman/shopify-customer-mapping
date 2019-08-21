from flask import (jsonify, url_for)
import json
import requests
import zipcodes
import pycurl

from app.gen.mymap import script
from config import Config


def get_response(shop, endpoint, params=''):
    if params == '':
        response = requests.get("%s%s" % (shop, endpoint))
    else:
        response = requests.get("%s%s&%s" % (shop, endpoint, params))
    return response


def get_theme_id(shop):
    theme_response = get_response(shop, "themes.json")
    all_themes = json.loads(theme_response.content.decode('utf-8')).get('themes')
    for theme in all_themes:
        if theme['role'] == "main":
            theme_id = theme['id']
            return theme_id
    return "No theme has the role of main"


def put_data(shop, endpoint, put_location, data):
    response = None
    headers= {"Accept": "text/plain", "Content-Type": "text/plain"}
    payload = {
      "asset": {
        "key": "assets/map.js",
        "attachment": script
      }
    }

    try:
        response = requests.put("%s%s" % (shop, endpoint), data=script, headers=headers)

        if response.status_code != 200:
            print(response.text)
            print(response.status_code)
            raise Exception('Recieved non 200 response.')
        return
    except requests.exceptions.RequestException as e:
        if response != None:
            print(response.text)
        print(e)
        raise

def put_data_curl(shop, endpoint, put_location, data):
    c = pycurl.Curl()

    url = "%s%s" %(shop, endpoint)
    print("URL: " + url)
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: text/plain', 'Accept: text/plain'])
    c.setopt(pycurl.CUSTOMREQUEST, "PUT")
    # data = script
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(c.UPLOAD, 1)
    file = open("app/gen/mymap.txt")
    c.setopt(c.READDATA, file)

    c.perform()
    print("status code: %s" % c.getinfo(pycurl.HTTP_CODE))
    c.close()

    file.close()

    return

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

        print("Order count is %s" %order_count)
        self.count = order_count
        return

    def set_order_locations(self):
        print(self.shop_url)
        location_endpoint = 'orders.json?limit=250&status=any'

        location_response = get_response(self.shop_url, location_endpoint)
        all_locations = json.loads(location_response.content.decode('utf-8')).get('orders')
        for address in all_locations:
            try:
                order_id = address['id']
                order_id_message = "ID is %s" % order_id
                print(order_id_message)
                created_at_message = "Created at: %s" % address['created_at']
                print(created_at_message)

                # print("Created at: %s" % address['created_at'])
                shipping_address = address['shipping_address']
                self.order_locations.append(shipping_address)
            except:
                try:
                    name = address['name']
                    message = "No address found for %s" % name
                    print(message)
                except:
                    message = "What's this? %s" % address
                    print(message)

        return

    def set_all_order_locations(self):
        order_count = self.count
        limit = 201
        current_order_count = 0
        min_date = ''

        location_endpoint = "orders.json?limit=%s&status=any" % limit
        location_response = get_response(self.shop_url, location_endpoint)

        if location_response.status_code == 200:
            all_locations = json.loads(location_response.content.decode('utf-8')).get('orders')
            count = 0
            for address in all_locations:
                try:
                    # print("count: " ,count)
                    if count == limit - 1:
                        min_date = address['created_at']
                        # print("Min Date is %s" % min_date)
                    else:
                        # order_id = address['id']
                        # order_id_message = "ID is %s" % order_id
                        # print(order_id_message)
                        # created_at_message = "Created at: %s" % address['created_at']
                        # print(created_at_message)

                        count += 1
                        shipping_address = address['shipping_address']
                        self.order_locations.append(shipping_address)
                except:
                    message = "Coulde not get address info"
                    print(message)
            current_order_count += limit - 1
        else:
            print("FAILED")

        # print("Order Locations after one run: ", self.order_locations)

        while current_order_count < order_count:
            location_endpoint = "orders.json?created_at_max=%s&limit=%s&status=any" % (min_date, limit)
            location_response = get_response(self.shop_url, location_endpoint)

            if location_response.status_code == 200:
                all_locations = json.loads(location_response.content.decode('utf-8')).get('orders')
                count = 0
                for address in all_locations:
                    try:
                        if count == limit - 1:
                            min_date = address['created_at']
                        else:
                            count += 1
                            shipping_address = address['shipping_address']
                            self.order_locations.append(shipping_address)
                    except:
                        message = "Coulde not get address info"
                        print(message)
                current_order_count += limit - 1
                print("COC: ", current_order_count)
            else:
                print("FAILED: ", location_response.status_code)

        return


    def put_data(self):
        theme_id = get_theme_id(self.shop_url)
        print("THEME ID =%s" % theme_id)
        endpoint = "themes/%s/assets.json" % theme_id
        file_location = "assets/map.js"
        print("SCRIPTE IS: " + script)
        # put_response = put_data(self.shop_url, endpoint, file_location, script)
        put_response = put_data_curl(self.shop_url, endpoint, file_location, script)
        print(put_response.status_code)
        print(put_response.headers)
        return json.loads(put_response.decode('utf-8'))


    def get_coordinates(self):
        all_coords = []

        for location in self.order_locations:
            lon = location['longitude']
            lat = location['latitude']

            current_coords = {'longitude': lon, 'latitude': lat}
            if current_coords not in all_coords:
                all_coords.append(current_coords)

        return all_coords

