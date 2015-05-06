import argparse
import pandas
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="the path to the .csv file")
    parser.add_argument("db", help="the path of the sqlite3 file to create")
    args = parser.parse_args()
    return args

def get_data(fname_data):
    df = pandas.read_csv(fname_data,
                         header=0, parse_dates="Timestamp",
                         index_col='Timestamp')
    print("  * data read from csv")
    df.fillna(-1, inplace=True)
    df[['x', 'y']] = df[['X', 'Y']].astype(np.int8)
    print("  * x y converted")
    df["movement"] = df["type"] == "movement"
    del df["type"]
    del df["X"]
    del df["Y"]
    print("  * movement converted")
    return df


def write_data(data, fname_db):
    data.to_hdf(fname_db,'df',mode='w',format='table')

def main():
    args = parse_args()
    fname_data, fname_db = args.data, args.db
    print("* get_data")
    data = get_data(fname_data)
    print("* write data")
    write_data(data, fname_db)

if __name__ == "__main__":
    main()
