#!/usr/bin/env python
"""

ZMQ Publisher for arduino sensor information
Queue: INF

"""
import datetime
from time import sleep
import json
import traceback
import sys
import zmq
import serial
import pprint

# this is the socket where we publish

zmqSocket = "tcp://*:5551"
serDevices = ["/dev/ttyACM0", "/dev/ttyACM1"]
# Initialize zmq
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(zmqSocket)

def read_sensors() :

    i = 0
    serDevice = serDevices[0]
    while True:
        try:
            ser = serial.Serial(serDevice, 9600)
            sensorReading = ser.readline();
            sensorReading = sensorReading.rstrip()
            sensorInfo =  json.loads(sensorReading)
            sensorInfo['readTimeString'] = datetime.datetime.now().strftime("%m/%d/%y %I:%M%p")
            sensorJSON = json.dumps(sensorInfo)
            #pp = pprint.PrettyPrinter(indent=4)
            #print pp.pprint(sensorJSON)
            socket.send_multipart(['INF_SENSOR',sensorJSON])
            return True

        except serial.serialutil.SerialException:
            i = i + 1
            if i > len(serDevices) - 1: 
                raise
            else:
                serDevice = serDevices[i]
                continue


def main_pub_inf_arduino_sensor() :

    exception_count = 0
    while True:
        try: 
            success = read_sensors()
            if success:
                exception_count = 0
            
        except KeyboardInterrupt:
            print ("Exit by KeyboardInterrupt\n")
            break
            
        # tolerate 20 minutes of disconnection
        except serial.serialutil.SerialException:
            exception_count = exception_count + 1
            if (exception_count > 20):
                raise
            else:
                print "Serial disconnected - waiting and re-trying "
                sleep(60)
                continue
        

if __name__ == '__main__':
    main_pub_inf_arduino_sensor()
