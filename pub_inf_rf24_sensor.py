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
from RF24 import *

# this is the socket where we publish

zmqSocket = "tcp://*:5551"
serDevices = ["/dev/ttyACM0", "/dev/ttyACM1"]
# Initialize zmq
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(zmqSocket)

# intitalize rf24 radio
# output pin is pin 29 on Rpi
radio = RF24(RPI_BPLUS_GPIO_J8_29, RPI_BPLUS_GPIO_J8_24,BCM2835_SPI_SPEED_8MHZ)
pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5,15)
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1,pipes[0])
radio.startListening()

def read_sensors() :
        
    # initialize array for output
    sensorInfo = {}
    start_seen = False
    while True:
        while radio.available():
            # Fetch the payload, and see if this was the last one.
            len = radio.getDynamicPayloadSize()
            receive_payload = radio.read(len)
            receive_payload = receive_payload.rstrip('\t\r\n\0')
            print receive_payload
            # wait for the START indicator which indicates a new packet
            if (receive_payload.strip() == 'START'):
                output = {} 
                start_seen = True
            elif (receive_payload == 'END'):
                if (start_seen):
                    sensorInfo['readTimeString'] = datetime.datetime.now().strftime("%m/%d/%y %I:%M%p")
                    sensorJSON = json.dumps(sensorInfo)
                    socket.send_multipart(['INF_SENSOR',sensorJSON])
                    print "sent"
                    return True
            else:
                info = json.loads(receive_payload)
                for key in info.keys():
                    sensorInfo[key] = info[key]
        
    return False

def main_pub_inf_rf24_sensor() :

    exception_count = 0
    while True:
        try: 
            success = read_sensors()
            if success:
                exception_count = 0
            	sleep(5)
	    else:
                print "Radio disconnected - waiting and re-trying "
                sleep(60)
                
        except KeyboardInterrupt:
            print ("Exit by KeyboardInterrupt\n")
            break
                    
        # tolerate 20 minutes of disconnection
        # except:
        #     exception_count = exception_count + 1
        #     if (exception_count > 20):
        #         radio.stopListening()
        #         raise
        #     else:
        #         print "Radio disconnected - waiting and re-trying "
        #         sleep(60)
        #         continue
                        

if __name__ == '__main__':
    main_pub_inf_rf24_sensor()
