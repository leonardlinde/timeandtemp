#!/usr/bin/env python
"""

ZMQ Subscriber for office sensor information - writes a json file
Queue: INF

"""
import gspreadwrite
import json
import zmq
import time

infSocket = "tcp://localhost:5550"
measurements = {'temperatureF':'t', 'humidity':'h', 
'pressure':'p','lux':'l'}


def main_sub_json_file():
    # Initialize zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(infSocket)
    socket.setsockopt(zmq.SUBSCRIBE, 'INF_SENSOR')

    last_write = 0
    try:
        while True:
            [cmd,dataIn] = socket.recv_multipart()
            officeData = json.loads(dataIn)
            arrived = True
            for measurement in measurements:
                if not (measurement in officeData):
                    arrived = False
            if not arrived:
                continue
            # every 5 minutes, or at the start, upload
            if (last_write == 0 or time.time() - last_write  >= 300):
                # throw out a json file for use in API stuff
                jsonfile = open('/home/pi/timeandtemp/officestats.json', 'w')
                jsonstring =  json.dumps({'h':officeData['humidity'],
                                          't':officeData['temperatureF'],
                                          'l':officeData['lux'],
                                          'p':officeData['pressure'],
                                          'now':officeData['readTimeString']})
                jsonfile.write(jsonstring)
                jsonfile.close()
                last_write  = time.time()

    except KeyboardInterrupt:
        print ("Exit by KeyboardInterrupt\n")

if __name__ == '__main__':
    main_sub_json_file()
