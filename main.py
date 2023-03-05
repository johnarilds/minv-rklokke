from machine import Pin#, SoftI2C
#import ssd1306
from time import sleep
import ujson
import network, time
import urequests
import ntptime 

#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

#oled_width = 128
#oled_height = 64
#oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

IN1 = Pin(5,Pin.OUT)
IN2 = Pin(18,Pin.OUT)
IN3 = Pin(19,Pin.OUT)
IN4 = Pin(21,Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
sequence_reverse = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]

viser_posisjon = 0

mapping = """{
    "clearsky":0,
    "fair":0,
    "partlycloudy":1,
    "rainshowers":2,
    "lightrainshowers":2,
    "rain":3,
    "lightrain":3,
    "heavyrain":4,
    "heavyrainshowers":4,
    "fog":5,
    "rainshowersandthunder":6,
    "heavyrainandthunder":6,
    "rainandthunder":6,
    "lightrainshowersandthunder":6,
    "heavyrainshowersandthunder":6,
    "lightrainandthunder":6,
    "sleetshowersandthunder":6,
    "sleetandthunder":6,
    "lightssleetshowersandthunder":6,
    "heavysleetshowersandthunder":6,
    "lightsleetandthunder":6,
    "heavysleetandthunder":6,
    "snowandthunder":6,
    "snowshowersandthunder":6,
    "lightssnowshowersandthunder":6,
    "heavysnowshowersandthunder":6,
    "lightsnowandthunder":6,
    "heavysnowandthunder":6,
    "sleetshowers":9,
    "lightsleetshowers":9,
    "sleet":10,
    "lightsleet":10,
    "heavysleet":11,
    "heavysleetshowers":11,
    "heavysnow":12,
    "heavysnowshowers":12,
    "snow":13,
    "lightsnow":13,
    "snowshowers":14,
    "lightsnowshowers":14,
    "cloudy":15,
    "clearsky_day":0,
    "fair_day":0,
    "partlycloudy_day":1,
    "rainshowers_day":2,
    "lightrainshowers_day":2,
    "rain_day":3,
    "lightrain_day":3,
    "heavyrain_day":4,
    "heavyrainshowers_day":4,
    "fog_day":5,
    "rainshowersandthunder_day":6,
    "heavyrainandthunder_day":6,
    "rainandthunder_day":6,
    "lightrainshowersandthunder_day":6,
    "heavyrainshowersandthunder_day":6,
    "lightrainandthunder_day":6,
    "sleetshowersandthunder_day":6,
    "sleetandthunder_day":6,
    "lightssleetshowersandthunder_day":6,
    "heavysleetshowersandthunder_day":6,
    "lightsleetandthunder_day":6,
    "heavysleetandthunder_day":6,
    "snowandthunder_day":6,
    "snowshowersandthunder_day":6,
    "lightssnowshowersandthunder_day":6,
    "heavysnowshowersandthunder_day":6,
    "lightsnowandthunder_day":6,
    "heavysnowandthunder_day":6,
    "sleetshowers_day":9,
    "lightsleetshowers_day":9,
    "sleet_day":10,
    "lightsleet_day":10,
    "heavysleet_day":11,
    "heavysleetshowers_day":11,
    "heavysnow_day":12,
    "heavysnowshowers_day":12,
    "snow_day":13,
    "lightsnow_day":13,
    "snowshowers_day":14,
    "lightsnowshowers_day":14,
    "cloudy_day":15,
    "clearsky_night":8,
    "fair_night":8,
    "partlycloudy_night":7,
    "rainshowers_night":2,
    "lightrainshowers_night":2,
    "rain_night":3,
    "lightrain_night":3,
    "heavyrain_night":4,
    "heavyrainshowers_night":4,
    "fog_night":5,
    "rainshowersandthunder_night":6,
    "heavyrainandthunder_night":6,
    "rainandthunder_night":6,
    "lightrainshowersandthunder_night":6,
    "heavyrainshowersandthunder_night":6,
    "lightrainandthunder_night":6,
    "sleetshowersandthunder_night":6,
    "sleetandthunder_night":6,
    "lightssleetshowersandthunder_night":6,
    "heavysleetshowersandthunder_night":6,
    "lightsleetandthunder_night":6,
    "heavysleetandthunder_night":6,
    "snowandthunder_night":6,
    "snowshowersandthunder_night":6,
    "lightssnowshowersandthunder_night":6,
    "heavysnowshowersandthunder_night":6,
    "lightsnowandthunder_night":6,
    "heavysnowandthunder_night":6,
    "sleetshowers_night":9,
    "lightsleetshowers_night":9,
    "sleet_night":10,
    "lightsleet_night":10,
    "heavysleet_night":11,
    "heavysleetshowers_night":11,
    "heavysnow_night":12,
    "heavysnowshowers_night":12,
    "snow_night":13,
    "lightsnow_night":13,
    "snowshowers_night":14,
    "lightsnowshowers_night":14,
    "cloudy_night":15,
    "clearsky_polartwilight":8,
    "fair_polartwilight":8,
    "partlycloudy_polartwilight":7,
    "rainshowers_polartwilight":2,
    "lightrainshowers_polartwilight":2,
    "rain_polartwilight":3,
    "lightrain_polartwilight":3,
    "heavyrain_polartwilight":4,
    "heavyrainshowers_polartwilight":4,
    "fog_polartwilight":5,
    "rainshowersandthunder_polartwilight":6,
    "heavyrainandthunder_polartwilight":6,
    "rainandthunder_polartwilight":6,
    "lightrainshowersandthunder_polartwilight":6,
    "heavyrainshowersandthunder_polartwilight":6,
    "lightrainandthunder_polartwilight":6,
    "sleetshowersandthunder_polartwilight":6,
    "sleetandthunder_polartwilight":6,
    "lightssleetshowersandthunder_polartwilight":6,
    "heavysleetshowersandthunder_polartwilight":6,
    "lightsleetandthunder_polartwilight":6,
    "heavysleetandthunder_polartwilight":6,
    "snowandthunder_polartwilight":6,
    "snowshowersandthunder_polartwilight":6,
    "lightssnowshowersandthunder_polartwilight":6,
    "heavysnowshowersandthunder_polartwilight":6,
    "lightsnowandthunder_polartwilight":6,
    "heavysnowandthunder_polartwilight":6,
    "sleetshowers_polartwilight":9,
    "lightsleetshowers_polartwilight":9,
    "sleet_polartwilight":10,
    "lightsleet_polartwilight":10,
    "heavysleet_polartwilight":11,
    "heavysleetshowers_polartwilight":11,
    "heavysnow_polartwilight":12,
    "heavysnowshowers_polartwilight":12,
    "snow_polartwilight":13,
    "lightsnow_polartwilight":13,
    "snowshowers_polartwilight":14,
    "lightsnowshowers_polartwilight":14,
    "cloudy_polartwilight":15
}"""

response_test = """{"type":"Feature","geometry":{"type":"Point","coordinates":[18.9427,69.6827,58]},"properties":{"meta":{"updated_at":"2023-03-03T21:05:21Z","units":{"air_temperature":"celsius","precipitation_amount":"mm","precipitation_rate":"mm/h","relative_humidity":"%","wind_from_direction":"degrees","wind_speed":"m/s","wind_speed_of_gust":"m/s"},"radar_coverage":"ok"},"timeseries":[{"time":"2023-03-03T21:05:00Z","data":{"instant":{"details":{"air_temperature":-3.4,"precipitation_rate":0.0,"relative_humidity":78.1,"wind_from_direction":182.8,"wind_speed":7.0,"wind_speed_of_gust":10.7}},"next_1_hours":{"summary":{"symbol_code":"fair_night"},"details":{"precipitation_amount":0.0}}}},{"time":"2023-03-03T21:10:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:15:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:20:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:25:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:30:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:35:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:40:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:45:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:50:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T21:55:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:00:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:05:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:10:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:15:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:20:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:25:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:30:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:35:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:40:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:45:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:50:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}},{"time":"2023-03-03T22:55:00Z","data":{"instant":{"details":{"precipitation_rate":0.0}}}}]}}"""

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect('Wokwi-GUEST','')
print('kobler til wifi')
while not sta_if.isconnected(): time.sleep(1)
ntptime.settime()

#Hente nowcast fra YR og sjekke respons
#url = str('https://api.met.no/weatherapi/nowcast/2.0/complete?lat=69.6827&lon=18.9427')
#request = urequests.get(url)
#print(type(request))
#if (request.status_code) == 200:
#  response = request.json()
#  print('Data hentet')
#  print(type(response))
#else:
#    print('Feilkode ' + str(request.status_code),0 ,30)

#Bruk denne kun i testmodus
response = ujson.loads(response_test)

sta_if.active(False)
print('frakoblet wifi')

tekst_melding = (response["properties"]["timeseries"][0]["data"]["next_1_hours"]["summary"]["symbol_code"])
print(tekst_melding)
print(type(mapping))
mapped = ujson.loads(mapping)
print(type(mapped))
verdi = (mapped[tekst_melding])
print(verdi)

#Ta tiden på å flytte viseren. Kan flytte denne frem for å ta tiden på hele sekvensen
sekundteller_1 = time.time()

antall_steg = (verdi - viser_posisjon)
if (antall_steg >= 0):
    #gå antall steg fremover, sequence
    for i in range(0, (antall_steg * 32), 4):
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.003)
else:
    #gå antall steg bakover, sequence_reverse
    for i in range(0, ((0 - antall_steg) * 32), 4):
        for step in sequence_reverse:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.003)

viser_posisjon = verdi
print(viser_posisjon)
sekundteller_2 = time.time()
print(sekundteller_2 - sekundteller_1)
#Vent til det er gått ett minutt fra oppdateringen startet
time.sleep(60 - (sekundteller_2 - sekundteller_1))
