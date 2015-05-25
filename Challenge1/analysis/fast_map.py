#!/usr/bin/env python
import sqlite3
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.pylab import *

import os.path
fname = "save.p"

sleep_time = 0.00001

day = 'friday'
day_db = '../' + day + '.db'
con = sqlite3.connect(day_db)
cur = con.cursor()

plt.ion()

def visualize(pos_dict):
	plt.hold(False)
	colors = ('bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko')
	for k, ((x, y), i) in pos_dict.items():
		plt.plot(x, y, colors[int(k) % len(colors)])
		plt.hold(True)

	plt.ylim(0, 100)
	plt.xlim(0, 100)
	plt.show()
	draw()
	#_ = raw_input("Press [enter] to continue.")
	time.sleep(sleep_time)

cur.execute("SELECT strftime('%s', time), id, status, x, y FROM spatial_data")

pos_dict = {}
last_time = 0
for i, row in enumerate(cur):
	x = row[3]
	y = row[4]
	t = row[0]
	pos_dict[row[1]] = ((x, y), t)
	if t != last_time:
		last_time = t
		visualize(pos_dict)

print "Done"