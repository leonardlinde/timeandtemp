#!/bin/bash
/home/pi/timeandtemp/zmq/proxy_info.py &
/home/pi/timeandtemp/zmq/pub_inf_rf24_sensor.py &
/home/pi/timeandtemp/zmq/sub_1602_display.py &
/home/pi/timeandtemp/zmq/sub_json_file.py &
/home/pi/timeandtemp/zmq/sub_initialstate.py &
