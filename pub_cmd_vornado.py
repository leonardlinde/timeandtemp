#!/usr/bin/env python
"""

ZMQ Publisher for commands from Vornado IR remote
Queue: INF

"""
import json
import traceback
import sys
import zmq
import lirc
import pprint
from RF24 import *

# this is the socket where we publish

zmqSocket = "tcp://*:5561"

# Initialize zmq
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(zmqSocket)

# Initialize our lirc read socket
sockid = lirc.init('leonard')

# Valid commands - translates Vornado keys to commands
commands = {'power':'toggleBacklight', 'pageup':'displayUp', 'pagedown': 'displayDown'}

def sendCommand(cmdArray):
    cmd = cmdArray.pop();
    if cmd in commands:
        socket.send_multipart(['CMD_LCD',commands[cmd]])
    else:
        print "Command "+cmd+" not implemented"
        

def main_pub_cmd_vornado() :

    try:
        while True:
            cmdArray = lirc.nextcode()
            # lirc sends an empty array when a button is held down
            # ignore those
            if len(cmdArray) > 0:
                sendCommand(cmdArray)

    except KeyboardInterrupt:
        print ("Exit by KeyboardInterrupt\n")

                        

if __name__ == '__main__':
    main_pub_cmd_vornado()
