import sqlite3

import pandas as pandas

from Core.settings import SQLitePath


def connect_to_SQLite():
    conn = sqlite3.connect(SQLitePath)
    return conn.cursor()


def update_auction_listings_table(cursor):
    cursor.execute('delete from auctionhouse_auctionlisting;')
    cursor.close()
    df = pandas.read_csv('/home/doom/PycharmProjects/SkyblockAPIInterpreter/Downloads/test.csv', index_col=False)
    df.to_sql('auctionhouse_auctionlisting', conn, if_exists='append', index=False)
