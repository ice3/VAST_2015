import sqlite3
import pandas
from matplotlib import pylab as plt

def get_data(fname, table, nb_lines):
    conn = sqlite3.connect(fname)
    sql_request = "SELECT * FROM {} LIMIT {}".format(table, nb_lines)
    df = pandas.read_sql(sql_request, conn, parse_dates="time", index_col='time')
    return df #.set_index('time')

df = get_data("./saturday.db", "spatial_data", 500000)

# # resample - aggregate
# bars = ticks.Price.resample('1min', how='ohlc')

# # indexing
# vwap.ix['2011-11-01 09:27':'2011-11-01 09:32']
# vwap.between_time('10:00', '16:00') # for the same day
# # or
# bars.open.at_time('9:30')


for group, data in df.groupby(df.index.map(lambda t: t.minute)):
	all_mat = np.zeros((100,100), dtype=np.int)
	for x, y in zip(data.x, data.y):
		all_mat[x, y] += 1
	all_mat = all_mat*1.0/len(data)
	plt.matshow(all_mat)
	plt.title(data.ix[0].name)
	print("saving: ", group)
	plt.savefig("{:02}.png".format(group))



len(df2[df2.status=="movement"])
len(df2[df2.status=="check-in"])

plt.plot(df2[df2.status=="check-in"].x, df2[df2.status=="check-in"].y)
plt.show()

