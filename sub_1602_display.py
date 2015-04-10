#!/usr/bin/env python
"""

ZMQ Subscriber for 1602 display
Queue: INF and CMD

"""
import wiringpi2 as wiringpi
import datetime
import time
import json
import Adafruit_DHT
import traceback
import zmq
import sys
import pprint

infoSocket = "tcp://localhost:5550"
cmdSocket  = "tcp://localhost:5560"

wiringpi.wiringPiSetup()  
# Initialize mcp3008 (same as 3004) ADC - first parm is pin base (must be > 64)
# Second param is SPI bus number
wiringpi.mcp3004Setup(100,0)
    
# Initialize LCD
# 2 rows of 16 columns, driven by 4 bits
# Control pins are WiringPi 15 & 16
# Data pins are WiringPi 0,1,2,3
display = wiringpi.lcdInit (2, 16, 4, 15,16, 0,1,2,3,0,0,0,0)

# LCD Backlight
backlightPin = 26 # GPIO12 is set to ground to turn off backlight
wiringpi.pinMode(backlightPin,1) #output
wiringpi.digitalWrite(backlightPin, 0)

# Init zmq
context = zmq.Context()

# Subscribe to all the info queues
info = context.socket(zmq.SUB)
info.connect(infoSocket)
info.setsockopt(zmq.SUBSCRIBE, 'INF_SENSOR')
info.setsockopt(zmq.SUBSCRIBE, 'INF_CURRENTWX')
info.setsockopt(zmq.SUBSCRIBE, 'INF_FORECASTWX')

# Subscribe to LCD command queue
cmd = context.socket(zmq.SUB)
cmd.connect(cmdSocket)
cmd.setsockopt(zmq.SUBSCRIBE, 'CMD_LCD')

# set up a poller to read both sockets
poller = zmq.Poller()
poller.register(info, zmq.POLLIN)
poller.register(cmd, zmq.POLLIN)

# state variables
commandState = {'backlight':True}


# convert ADC reading to Lux
def rawToLux( raw ):
    # Range for converting the output of the light sensor on the
    # ADC to lux
    rawRange = 1024   # 
    logRange = 5.0    # 3.3 V = 10^5 Lux

    logLux = raw * logRange / rawRange
    return round(pow(10, logLux))

def processSensor(dataIn):
    officeData = json.loads(dataIn)
    
    wiringpi.lcdPosition(display, 0,0)
    now = datetime.datetime.now().strftime("%m/%d/%y %I:%M%p")
    wiringpi.lcdPuts(display, now)
    if 'temperatureF' in officeData and 'humidity' in officeData:
        out =  "%3dF %2d%%" % (officeData['temperatureF'], officeData['humidity'])
        wiringpi.lcdPosition(display, 0,1)
        wiringpi.lcdPuts(display, out)
    else:
        print "Temp/Humidity missing"
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(officeData)
        
    if 'lux' in officeData:
        wiringpi.lcdPosition(display, 9,1)
        out = "%4d lx" % (officeData['lux'])
        wiringpi.lcdPuts(display, out)
    else:
        print "lux missing"
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(officeData)

def processCommand(command):
    # if backlight is on, turn it off
    if command == 'toggleBacklight':
        if commandState['backlight']:
            wiringpi.digitalWrite(backlightPin, 1)
            commandState['backlight'] = False
        else:
            wiringpi.digitalWrite(backlightPin, 0)
            commandState['backlight'] = True

def main_sub_1602_display():

    while True:
        try:
            socks = dict(poller.poll())

        except KeyboardInterrupt:
            print ("Exit by KeyboardInterrupt\n")
            exit

        if cmd in socks:
            [queue, dataIn] = cmd.recv_multipart()
            processCommand(dataIn)

        if info in socks:
            [queue, dataIn] = info.recv_multipart()
            if queue == 'INF_SENSOR':
                processSensor(dataIn)

if __name__ == '__main__':
    main_sub_1602_display()
