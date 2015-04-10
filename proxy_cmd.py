#!/usr/bin/env python
"""

ZMQ proxy for cmd queues. 
Publish Queue: tcp:5560

"""
import zmq

# these are the ports we are doing proxy for
proxies = ['5561']

def main_proxy_info():
    ctx = zmq.Context()
    frontend = ctx.socket(zmq.XSUB)
    for proxy in proxies:
        queue = "tcp://localhost:" + proxy
        frontend.connect(queue)
    backend = ctx.socket(zmq.XPUB)
    backend.bind("tcp://*:5560")
    zmq.proxy(frontend,backend)


if __name__ == '__main__':
    main_proxy_info()
