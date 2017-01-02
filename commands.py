from datetime import datetime
import urllib2
import json
import pyowm

with open('../keys.json', 'r') as file_pointer:
    json_object=json.load(open('../keys.json','r'))

#Finds the Current Temperature of either your location or a location that you specify.
def currenttemperature(aExtraction):
    owm = pyowm.OWM(str(json_object["OWM_KEY"]))
    finalLocation = alchemyFindLocation(aExtraction)
    observation = owm.weather_at_place(finalLocation)
    w = observation.get_weather()
    z = w.get_temperature('fahrenheit')
    print(w)
    print(z['temp'])
    return "The temperature in " + finalLocation + " is " + str(z['temp']) + " degrees fahrenheit."

#Tells you some basic weather information with the same location parameters as with the currenttemperature() function.
def currentweather(aExtraction):
    owm = pyowm.OWM(str(json_object["OWM_KEY"]))
    finalLocation = alchemyFindLocation(aExtraction)
    observation = owm.weather_at_place(finalLocation)
    w = observation.get_weather()
    detailedObservation = w.get_detailed_status()
    z = w.get_temperature('fahrenheit')
    temperature = z['temp']
    s = w.get_wind()
    windSpeed = s['speed']
    print(z)
    return "The weather in " + finalLocation + " is " + str(detailedObservation) + " with a temperature of " + str(temperature) + " degrees fahrenheit, with a wind speed of " + str(windSpeed) + " meters per second."

#Tells you the time
def time(aExtraction):
    now = datetime.now()
    time = str(now.hour) + ":" + str(now.minute)
    return time

#Tells you your current location
def location(aExtraction):
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

#Takes an alchemy call and, if it is valid, returns a location. If it isn't, it returns your current location.
def alchemyFindLocation(aExtraction):
    if aExtraction['status'] == 'OK':
        placeFound = False
        for entity in aExtraction['entities']:
            if entity['type'] == "City" or entity['type'] == "StateOrCounty" or entity['type'] == "Country":
                print('text: ', entity['text'].encode('utf-8'))
                print('type: ', entity['type'])
                # print('relevance: ', entity['relevance'])
                # print('sentiment: ', entity['sentiment']['type'])
                # if 'score' in entity['sentiment']:
                #     print('sentiment score: ' + entity['sentiment']['score'])
                # print('')
                placeFound = True
                location = entity['text'].encode('utf-8')
                break
        if placeFound:
            finalLocation = str(location)
        else:
            f = urllib2.urlopen('http://freegeoip.net/json/')
            json_string = f.read()
            f.close()
            location = json.loads(json_string)
            finalLocation = str(location['city'])
    else:
        print("Problem with alchemy api.")
        f = urllib2.urlopen('http://freegeoip.net/json/')
        json_string = f.read()
        f.close()
        location = json.loads(json_string)
        finalLocation = str(location['city'])
    return finalLocation

#Calls a function from this file.
def call(name, aExtraction):
    return globals()[name](aExtraction)
