import argparse
import dateutil
import dateutil.parser
import sqlite3

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("data")
    parser.add_argument("db")
    args = parser.parse_args()
    return args

def get_data(fname_data):
    i = 0
    with open(fname_data, "r") as f:
        # we skip the header
        f.next()
        for line in f:
            res = line.strip().split(',')
            try:
                res = (dateutil.parser.parse(res[0]),
                   int(res[1]),
                   res[2],
                   int(res[3]), int(res[4]))
            except:
                print("error on line : {} - {}".format(i, line))
            else:
                i += 1
                if (i % 100 == 0): print("processed {} lines".format(i))
                yield res

def write_data(data, fname_db):
    conn = sqlite3.connect(fname_db, detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS spatial_data
                (time timestamp, id int, status text, x int, y int)''')
    c.executemany("INSERT INTO spatial_data VALUES(?, ?, ?, ?, ?)", data)
    conn.commit()
    c.close()

def main():
    args = parse_args()
    fname_data, fname_db = args.data, args.db
    data = get_data(fname_data)
    write_data(data, fname_db)

if __name__ == "__main__":
    main()
