import sqlite3

import pandas as pandas

from Core.settings import SQLitePath, CSVDownloadsPath


def connect_to_SQLite():
    conn = sqlite3.connect(SQLitePath)
    return conn


def update_auction_listings_table(cursor, conn):
    cursor.execute('delete from auctionhouse_auctionlisting;')
    cursor.close()
    df = pandas.read_csv(CSVDownloadsPath + 'auction_data.csv', index_col=False)
    df.to_sql('auctionhouse_auctionlisting', conn, if_exists='append', index=False)


def update_bazaar_bazaarquickstatus_table(cursor, conn):
    cursor.execute('delete from bazaar_bazaarquickstatus;')
    cursor.close()
    df = pandas.read_csv(CSVDownloadsPath + 'quick_status.csv', index_col=False)
    df.to_sql('bazaar_bazaarquickstatus', conn, if_exists='append', index=False)


def update_bazaar_bazaarbuysummary_table(cursor, conn):
    cursor.execute('delete from bazaar_bazaarbuysummary;')
    cursor.close()
    df = pandas.read_csv(CSVDownloadsPath + 'buy_summary.csv', index_col=False)
    df.to_sql('bazaar_bazaarbuysummary', conn, if_exists='append', index=False)


def update_bazaar_bazaarsellsummary_table(cursor, conn):
    cursor.execute('delete from bazaar_bazaarsellsummary;')
    cursor.close()
    df = pandas.read_csv(CSVDownloadsPath + 'sell_summary.csv', index_col=False)
    df.to_sql('bazaar_bazaarsellsummary', conn, if_exists='append', index=False)

def update_bazaar_bazaarlisting_table(cursor, conn):
    cursor.execute('delete from bazaar_bazaarlisting;')
    cursor.close()
    df = pandas.read_csv(CSVDownloadsPath + 'bazaar_listing.csv', index_col=False)
    df.to_sql('bazaar_bazaarlisting', conn, if_exists='append', index=False)