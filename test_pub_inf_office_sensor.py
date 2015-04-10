#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq
import pprint

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from office sensor...")
socket.connect("tcp://localhost:5551")
socket.setsockopt(zmq.SUBSCRIBE, 'INF_SENSOR')


pp = pprint.PrettyPrinter()
while True:
    [cmd,data] = socket.recv_multipart()
    pp.pprint(cmd)
    pp.pprint(data)
