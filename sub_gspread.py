#!/usr/bin/env python
"""

ZMQ Subscriber for Google Spreadsheet write
Queue: INF

"""

import gspreadwrite
import json
import zmq

infSocket = "tcp://localhost:5550"

def main_sub_gspread():
    # Initialize zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(infSocket)
    socket.setsockopt(zmq.SUBSCRIBE, 'INF_SENSOR')
    
    count = 0
    try:
        while True:
            [cmd,dataIn] = socket.recv_multipart()
            officeData = json.loads(dataIn)
            # every 5 minutes, or at the start, upload
            if (count == 0 or count >= 60):
                gspreadwrite.addData(officeData['readTimeString'],
                                     officeData['temperatureF'], 
                                     officeData['humidity'], 
                                     officeData['lux'])
                count = 1
            count = count + 1
            
    except KeyboardInterrupt:
        print ("Exit by KeyboardInterrupt\n")

if __name__ == '__main__':
    main_sub_gspread()
