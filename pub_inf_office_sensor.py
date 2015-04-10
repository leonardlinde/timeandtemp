#!/usr/bin/env python
"""

ZMQ Publisher for office sensor information
Queue: INF

"""
import wiringpi2 as wiringpi
import datetime
import time
import json
import Adafruit_DHT
import traceback
import sys
import zmq

# this is the socket where we publish

zmqSocket = "tcp://*:5551"

# do an additional analog read
doAnalog = False

# convert ADC reading to Lux
def rawToLux( raw ):
    # Range for converting the output of the light sensor on the
    # ADC to lux
    rawRange = 1024   # 
    logRange = 5.0    # 3.3 V = 10^5 Lux

    logLux = raw * logRange / rawRange
    return round(pow(10, logLux))


def main_pub_inf_office_sensor() :
    # Initialize WiringPi 
    wiringpi.wiringPiSetup()  
    # Initialize mcp3004 ADC - first parm is pin base (must be > 64)
    # Second param is SPI bus number
    wiringpi.mcp3004Setup(100,0)

    # Initialize zmq
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(zmqSocket)


    try: 
        while True:
            sensorReading = {}
            sensorReading['readTimeString'] = datetime.datetime.now().strftime("%m/%d/%y %I:%M%p")
            # Try to grab a DHT22 sensor reading.  Use the read_retry method which will retry up
            # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            sensor = Adafruit_DHT.DHT22
            # pin is GPIO numbering, not wiringpi numbering
            humidity, temperature = Adafruit_DHT.read_retry(sensor, 12)
            sensorReading['temperatureF'] = round((1.8 * temperature) + 32)
            sensorReading['humidity'] = round(humidity,1)
            
            # ADC read
            # pin 0 is lux meter 100 + 0 = 100
            value = wiringpi.analogRead(100)
            sensorReading['lux'] = rawToLux(value)

            if doAnalog == True:
                # pin 2 is analog temp
                value = wiringpi.analogRead(102)
                atemp = (((value / 1024.0) * 3.3) * 100.0) - 50
                sensorReading['temperatureC'] = round(atemp,1)
            sensorString = json.dumps(sensorReading)
            socket.send_multipart(['INF_SENSOR',sensorString])
            time.sleep(5)

    except KeyboardInterrupt:
        print ("Exit by KeyboardInterrupt\n")

if __name__ == '__main__':
    main_pub_inf_office_sensor()
