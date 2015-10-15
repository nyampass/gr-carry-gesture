#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import serial
import time
import random
from collections import deque
import numpy as np
import threading

data = deque()

def byte2value(l, h):
    v = float((l | (h & 0x7f) << 8) - 32768) if (h & 0x80) > 0 else float(h << 8 | l)
    return v * 0.00006

com = serial.Serial('/dev/cu.usbserial-A901OD69',
                    baudrate=115200, bytesize=8,
                    parity='N', stopbits=1,xonxoff=0, dsrdtr=0, timeout=1.0)
com.setDTR(False)

log_mode = False

def save_with_type(type):
    f = open('./data/gesture_{0}_{1}.csv'.format(type, time.time()), 'w')
    for line in data:
        f.write(line)
    f.close

def receive_commnad():
    global t, log_mode
    while True:
        raw_input("start record.[enter]: ")
        print "start recording... "
        data.clear()
        t = 0
        log_mode = True
        time.sleep(2.0)
        log_mode = False
        print "done.",
        command = raw_input(
            "save type[c: circle / 1: one / 2: two: / h: horizon / w: wait / other: not save]: ")
        if command in {"c", "1", "2", "-", "w"}:
            save_with_type(command)

th = threading.Thread(target=receive_commnad)
th.setDaemon(True)
th.start()

t = 0
while True:
    bytes = map(ord, com.read(6))
    if len(bytes) >= 6:
        if log_mode:
            print log_mode
            axis = '{0},{1},{2},{3}\r\n'.format(
                t,
                byte2value(bytes[0], bytes[1]),
                byte2value(bytes[2], bytes[3]),
                byte2value(bytes[4], bytes[5]))
            print axis
            data.append(axis)
    else:
        print "cant get data"
    com.write('b')
    t += 1
    time.sleep(0.00001)
