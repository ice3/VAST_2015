#!/usr/bin/env python
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import *

day = 'friday'
day_db = '../' + day + '.db'
con = sqlite3.connect(day_db)
cur = con.cursor()

plt.ion()

all_mat = np.zeros((100,100), dtype=np.int)
ch_mat = np.zeros((100,100), dtype=np.int)


def visualize(row):
	plt.hold(False)
	plt.plot(row[3], row[4], 'ro')
	plt.show()
	plt.ylim(0, 100)
	plt.xlim(0, 100)
	_ = raw_input("Press [enter] to continue.")


cur.execute("SELECT * FROM spatial_data")
for i, row in enumerate(cur):
	if i % 100000 == 0:
		print i
	#visualize(row)
	all_mat[row[3]][row[4]] += 1
	#print row
	#print all_mat
cur.execute("SELECT * FROM spatial_data WHERE status='check-in'")
for i, row in enumerate(cur):
	ch_mat[row[3]][row[4]] += 1
con.close()

matshow(all_mat, fignum=1, cmap=cm.gray)
_ = raw_input("Press [enter] to continue.")

matshow(ch_mat, fignum=1, cmap=cm.gray)
_ = raw_input("Press [enter] to continue.")

np.save(day, all_mat)
np.save(day + '-checkins', ch_mat)