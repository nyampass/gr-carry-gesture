#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets, metrics
import re
from glob import glob
import csv
import random
from itertools import chain
from sklearn.externals import joblib

y = []
keymap = {"1": 1, "2": 2, "h": 0, "c": 3, "w": 4}

X = []
files = glob('./data/gesture_*.csv')
random.shuffle(files)
for filename in files:
    m = re.search(r'gesture_(\S+)_([\d\.]+)\.csv', filename)
    if m:
        y.append(keymap[m.group(1)])
        data = []
        for row in csv.reader(open(filename, 'rb')):
            for field in map(float, row)[1:]:
                data.append(field)
        X.append(data)

X = np.array(X)
min_len = min(map(len, X))
X = np.array(map(lambda x:np.array(x[:min_len], dtype=float).reshape(min_len / 1, 1)[:, :1].reshape(1, min_len / 1)[0], X))

n_samples = len(X)

classifier = svm.SVC(kernel='poly', degree=3, C=1e3)

classifier.fit(X[:n_samples / 2], y[:n_samples / 2])

expected = y[n_samples / 2:]
predicted = classifier.predict(X[n_samples / 2:])

print("Classification report [%s]:\n%s\n"
    % (classifier,
       metrics.classification_report(expected, predicted)
    )
)
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

joblib.dump(classifier, 'gesture-class.pkl')

exit()
