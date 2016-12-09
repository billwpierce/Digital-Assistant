from datetime import datetime
import urllib2
import json


def time():
    return datetime.now().time()
def location():
    f = urllib2.urlopen('http://freegeoip.net/json/')
    json_string = f.read()
    f.close()
    location = json.loads(json_string)
    location_city = location['city']
    location_state = location['region_name']
    location_country = location['country_name']
    location_zip = location['zip_code']
    finallocation = "You are in " + str(location_city) + ", " + str(location_state) + "."
    return finallocation
def call(name):
    return globals()[name]()
