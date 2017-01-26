from datetime import datetime
import urllib2
import json
import pyowm
import subprocess

with open('../keys.json', 'r') as file_pointer:
    json_object=json.load(open('../keys.json','r'))

#Finds the Current Temperature of either your location or a location that you specify.
def currenttemperature(aExtraction):
    owm = pyowm.OWM(str(json_object["OWM_KEY"]))
    finalLocation = alchemyFindLocation(aExtraction)
    observation = owm.weather_at_place(finalLocation)
    w = observation.get_weather()
    z = w.get_temperature('celsius')
    print(z)
    # print(z['temp'])
    return "The temperature in " + finalLocation + " is " + str(z['temp']) + " degrees celsius."

#Tells you some basic weather information with the same location parameters as with the currenttemperature() function.
def currentweather(aExtraction):
    owm = pyowm.OWM(str(json_object["OWM_KEY"]))
    finalLocation = alchemyFindLocation(aExtraction)
    print finalLocation
    observation = owm.weather_at_place(finalLocation)
    w = observation.get_weather()
    detailedObservation = w.get_detailed_status()
    z = w.get_temperature('celsius')
    temperature = z['temp']
    s = w.get_wind()
    windSpeed = s['speed']
    print(z)
    return "The weather in " + finalLocation + " is " + str(detailedObservation) + " with a temperature of " + str(temperature) + " degrees celsius, with a wind speed of " + str(windSpeed) + " meters per second."

#Tells you the time
def time(aExtraction):
    now = datetime.now()
    time = str(now.hour) + ":" + str(now.minute)
    return time

#Tells you your current location
def location(aExtraction):
    location = locationFromIP()
    location_city = location['city']
    location_state = location['region']
    location_country = location['country']
    location_zip = location['postal']
    finallocation = "You are in " + str(location_city) + ", " + str(location_state) + "."
    return finallocation

#Takes an alchemy call and, if it is valid, returns a location. If it isn't, it returns your current location.
def alchemyFindLocation(aExtraction):
    if aExtraction['status'] == 'OK':
        placeFound = False
        for entity in aExtraction['entities']:
            if entity['type'] == "City" or entity['type'] == "StateOrCounty" or entity['type'] == "Country":
                print('text: ', entity['text'].encode('utf-8'))
                print('type: ', entity['type'])
                placeFound = True
                location = entity['text'].encode('utf-8')
                break
        if placeFound:
            finalLocation = str(location)
        else:
            location_stuff = locationFromIP()
            finalLocation = location_stuff
    else:
        print("Problem with alchemy api.")
        location_city = locationFromIP()
        finalLocation = location_city
    return finalLocation

#Returns general location from ip
def locationFromIP():
    ipinfoio = subprocess.check_output(["curl","ipinfo.io"])
    ip = json.loads(ipinfoio)
    return str(ip['city'] + " " + ip['region'])

#Calls a function from this file.
def call(name, aExtraction):
    return globals()[name](aExtraction)
