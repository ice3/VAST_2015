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

def create_heatmaps(df, key=lambda t: t.minute):
	for group, data in df.groupby(df.index.map(key)):
		all_mat = np.zeros((100,100), dtype=np.int)
		for x, y in zip(data.x, data.y):
			all_mat[x, y] += 1
		all_mat = all_mat*1.0/len(data)
		plt.matshow(all_mat)
		plt.title(data.ix[0].name)
		print("saving: ", group)
		plt.savefig("{:02}.png".format(group))

create_heatmaps(df)

def create_path_id(df, ids):
	def getId(i): return df[df.id==i]
	for id_ in ids:
		plt.scatter(getId(id_).x,
			     getId(id_).y,
			     label = str(id_))
	plt.legend()

id_unique = df.id.unique()
create_path_id(df, id_unique[:10])

plt.plot(df2[df2.status=="check-in"].x, df2[df2.status=="check-in"].y)
plt.show()

