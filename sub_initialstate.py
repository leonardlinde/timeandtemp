#!/usr/bin/env python
"""

ZMQ Subscriber for Initialstate.com
Queue: INF

"""

import json
import zmq
import time
import datetime
from ISStreamer.Streamer import Streamer
 
streamer = Streamer(bucket_name="Office", bucket_key="sensors_v2", access_key="NjBSt9cnsbLjRu2MGK59092qAqKpfxzY")
infSocket = "tcp://localhost:5550"
measurements = {'temperatureF':'Temperature (F)', 'humidity':'Humidity (%)', 
'pressure':'Sea Level Pressure (HPa)','lux':'Brightness(Lx)'}

def main_sub_initialstate():
    # Initialize zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(infSocket)
    socket.setsockopt(zmq.SUBSCRIBE, 'INF_SENSOR')
    
    last_write = 0
    try:
        while True:
            [cmd,dataIn] = socket.recv_multipart()
            # every 5 minutes, or at the start, upload
            if (last_write == 0 or time.time() - last_write  >= 300):
                officeData = json.loads(dataIn)
                # check that all the keys arrived
                arrived = True
                for measurement in measurements:
                    if not (measurement in officeData):
                        arrived = False
                if arrived: 
                    for measurement in measurements:
                        streamer.log(measurements[measurement], officeData[measurement])
                    streamer.flush()
                    last_write = time.time()
                    print "Sent:" + datetime.datetime.now().strftime("%m/%d/%y %I:%M%p")
            
    except KeyboardInterrupt:
        print ("Exit by KeyboardInterrupt\n")
        streamer.close()

if __name__ == '__main__':
    main_sub_initialstate()

