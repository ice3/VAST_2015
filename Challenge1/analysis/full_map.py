#!/usr/bin/env python
import sqlite3
import numpy as np
import time as t
import datetime
import matplotlib.pyplot as plt
from matplotlib.pylab import *

import os.path
fname = "save.p"

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
		plt.show()
		plt.ylim(0, 100)
		plt.xlim(0, 100)
		plt.hold(True)
	_ = raw_input("Press [enter] to continue.")

def vis_data(all_dict, n):
	pos_dict = {}
	for i in range(n):
		for k, v in all_dict.items():
			if v[0][i] > -1:
				pos_dict[k] = ((v[0][i], v[1][i]), i)
		visualize(pos_dict)

	
cur.execute("SELECT strftime('%s', MIN(time)) FROM spatial_data")
min_t = int(cur.fetchone()[0])

cur.execute("SELECT strftime('%s', MAX(time)) - strftime('%s', MIN(time)) AS dif FROM spatial_data")
diff = int(cur.fetchone()[0]) + 1
	
all_dict = {}

cur.execute("SELECT strftime('%s', time), id, status, x, y FROM spatial_data")

for i, row in enumerate(cur):
	if i % 100000 == 0:
		print i
	#visualize(row)
	if row[1] in all_dict:
		xs = all_dict[row[1]][0]
		ys = all_dict[row[1]][1]
		time = int(row[0]) - min_t
		xs[time] = row[3]
		ys[time] = row[4]
	else:
		xs = -1 * np.ones(diff, dtype=np.int16) # Correct this, 0 is also valid
		ys = -1 * np.ones(diff, dtype=np.int16)
		time = int(row[0]) - min_t
		xs[time] = row[3]
		ys[time] = row[4]
		all_dict[row[1]] = [xs, ys]

print "Done"

vis_data(all_dict, diff)