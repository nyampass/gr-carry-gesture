#!/usr/bin/env python2.7

from subprocess import call, Popen
import sys, serial
import numpy as np
import time
from sklearn.externals import joblib
import os
import sys
from appscript import app, its, mactypes

def update(name):
    se = app('System Events')
    for desktop_name in se.desktops.display_name.get():
        desk = se.desktops[its.display_name == desktop_name]
        desk.picture.set(mactypes.File("./images/" + name))

classifier = joblib.load('gesture-class.pkl')

com = serial.Serial('/dev/cu.usbserial-A901OD69',
                    baudrate=115200, bytesize=8,
                    parity='N', stopbits=1,xonxoff=0, dsrdtr=0, timeout=1.0)
com.setDTR(False)

def byte2value(l, h):
    v = float((l | (h & 0x7f) << 8) - 32768) if (h & 0x80) > 0 else float(h << 8 | l)
    return v * 0.00006

event_map = {}
for k, v in {"1": 1, "2": 2, "h": 0, "c": 3, "w": 4}.items():
    event_map[v] = k

data_len = 750

data = []
t = 0
while True:
    bytes = map(ord, com.read(6))
    if len(bytes) >= 6:
        for v in [byte2value(bytes[0], bytes[1]),
                  byte2value(bytes[2], bytes[3]),
                  byte2value(bytes[4], bytes[5])]:
            data.append(v)
        if len(data) > data_len:
            for i in range(3):
                data.pop(0)
        if len(data) == data_len:
            ret = classifier.predict(np.array(data))
            if ret is not None and len(ret) > 0:
                event = event_map[ret[0]]
                if event is not "w":
                    print event, 
                    sys.stdout.flush()
                    if event == "1":
                        update("on.png")
                        call(["wemo", "switch", "wemo", "on"])
                    elif event == "h":
                        update("off.png")
                        call(["wemo", "switch", "wemo", "off"])
                    data = []
    else:
        print "cant get data"
    com.write('b')
    t += 1
    time.sleep(0.00001)
