from datetime import datetime
import urllib2
import json
import pyowm

with open('../keys.json', 'r') as file_pointer:
    json_object=json.load(open('../keys.json','r'))

def currenttemperature():
    # print("test")
    owm = pyowm.OWM(str(json_object["OWM_KEY"]))
    # print("test2")
    f = urllib2.urlopen('http://freegeoip.net/json/')
    json_string = f.read()
    f.close()
    location = json.loads(json_string)
    observation = owm.weather_at_place(str(location['city']) + "," + str(location['country_code']))
    w = observation.get_weather()
    z = w.get_temperature('fahrenheit')
    print(z)
    # far_json = z.read()
    # z.close()
    # temp = json.loads(str(z))
    print(z['temp'])
    return "The temperature is " + str(z['temp']) + " degrees fahrenheit."
def time():
    now = datetime.now()
    time = str(now.hour) + ":" + str(now.minute)
    return time
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
