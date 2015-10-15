#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import serial
import time
import random
from collections import deque
import numpy as np
import threading
import matplotlib.pyplot as plt

max = 100
data = []
for i in range(3):
    data.append(deque([0]*max, max))

def byte2value(l, h):
    v = float((l | (h & 0x7f) << 8) - 32768) if (h & 0x80) > 0 else float(h << 8 | l)
    return v * 0.00006

com = serial.Serial('/dev/cu.usbserial-A901OD69',
                    baudrate=115200, bytesize=8,
                    parity='N', stopbits=1,xonxoff=0, dsrdtr=0, timeout=1.0)
com.setDTR(False)

plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(-4, 4))
lines = [ax.plot([], [])[0] for i in range(3)]

t = 0
while True:
    bytes = map(ord, com.read(6))
    if len(bytes) >= 6:
        axis = [byte2value(bytes[0], bytes[1]),
                byte2value(bytes[2], bytes[3]),
                byte2value(bytes[4], bytes[5])]
        print axis
        for i in range(3):
            print data[i]
            data[i].append(axis[i])
            lines[i].set_data(range(max), data[i])
    com.write('b')
    t += 1
    time.sleep(0.00001)
    plt.pause(0.00001)
