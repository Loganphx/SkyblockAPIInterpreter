import csv
import json
import requests

from Core.settings import CSVDownloadsPath
from PythonScripts.SQLiteLibrary.SQLiteConnection import update_bazaar_bazaarquickstatus_table, connect_to_SQLite, \
    update_bazaar_bazaarsellsummary_table, update_bazaar_bazaarbuysummary_table, update_bazaar_bazaarlisting_table


def get_bazaar_data() -> json:
    x = requests.get('https://api.hypixel.net/skyblock/bazaar?key=41b2a888-f84c-4287-bf56-2012895c8e4d')
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    return json_loaded


def get_sell_summary(itemSellSummary, product_id):
    tempArray = []
    tempArray.append(product_id)
    tempArray.append(itemSellSummary['amount'])
    tempArray.append(itemSellSummary['pricePerUnit'])
    tempArray.append(itemSellSummary['orders'])
    return tempArray


def getSellSummaries(bazaar_data):
    sellArray = [['product_id', 'amount', 'pricePerUnit', 'orders']]
    for item in bazaar_data['products']:
        for item2 in bazaar_data['products'][item]['sell_summary']:
            sellArray.append(get_sell_summary(item2, item))
    return sellArray


def get_buy_summary(itemBuySummary, product_id):
    buyArray = []
    buyArray.append(product_id)
    buyArray.append(itemBuySummary['amount'])
    buyArray.append(itemBuySummary['pricePerUnit'])
    buyArray.append(itemBuySummary['orders'])
    return buyArray


def getBuySummaries(bazaar_data):
    buyArray = [['product_id', 'amount', 'pricePerUnit', 'orders']]
    for item in bazaar_data['products']:
        for item2 in bazaar_data['products'][item]['buy_summary']:
            buyArray.append(get_buy_summary(item2, item))
    return buyArray


def get_quick_status(itemQuickStatus, product_id):
    quickStatusArray = []
    quickStatusArray.append(product_id)
    quickStatusArray.append(itemQuickStatus['sellPrice'])
    quickStatusArray.append(itemQuickStatus['sellVolume'])
    quickStatusArray.append(itemQuickStatus['sellMovingWeek'])
    quickStatusArray.append(itemQuickStatus['sellOrders'])
    quickStatusArray.append(itemQuickStatus['buyPrice'])
    quickStatusArray.append(itemQuickStatus['buyVolume'])
    quickStatusArray.append(itemQuickStatus['buyMovingWeek'])
    quickStatusArray.append(itemQuickStatus['buyOrders'])
    return quickStatusArray


def getQuickStatuses(bazaar_data):
    quickStatusArray = [['product_id', 'sellPrice', 'sellVolume', 'sellMovingWeek', 'sellOrders',
                         'buyPrice', 'buyVolume', 'buyMovingWeek', 'buyOrders']]
    for item in bazaar_data['products']:
        tempArray = get_quick_status(bazaar_data['products'][item]['quick_status'], item)
        quickStatusArray.append(tempArray)
    return quickStatusArray


def write_quick_status_file(bazaar_data):
    with open(CSVDownloadsPath + 'quick_status.csv', 'w', newline='\n', encoding='utf-8') as foo:
        writer = csv.writer(foo)
        QuickStatusArray = getQuickStatuses(bazaar_data)
        writer.writerows(QuickStatusArray)


def write_sell_summary_file(bazaar_data):
    with open(CSVDownloadsPath + 'sell_summary.csv', 'w', newline='\n', encoding='utf-8') as foo:
        writer = csv.writer(foo)
        sellSummaryArray = getSellSummaries(bazaar_data)
        writer.writerows(sellSummaryArray)


def write_buy_summary_file(bazaar_data):
    with open(CSVDownloadsPath + 'buy_summary.csv', 'w', newline='\n', encoding='utf-8') as foo:
        writer = csv.writer(foo)
        buySummaryArray = getBuySummaries(bazaar_data)
        for item in buySummaryArray:
            writer.writerow(item)


bazaarData = get_bazaar_data()
write_buy_summary_file(bazaar_data=bazaarData)
write_sell_summary_file(bazaar_data=bazaarData)
write_quick_status_file(bazaar_data=bazaarData)

conn = connect_to_SQLite()
update_bazaar_bazaarquickstatus_table(cursor=conn.cursor(), conn=conn)
update_bazaar_bazaarbuysummary_table(cursor=conn.cursor(), conn=conn)
update_bazaar_bazaarsellsummary_table(cursor=conn.cursor(), conn=conn)
update_bazaar_bazaarlisting_table(cursor=conn.cursor(), conn=conn)

