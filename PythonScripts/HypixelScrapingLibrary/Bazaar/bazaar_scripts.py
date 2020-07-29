import csv
import json
import requests

from Core.settings import CSVDownloadsPath
from DjangoMicroservices.bazaar.models import BazaarBuySummary, BazaarSellSummary, BazaarQuickStatus
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


def write_bazaar_listing(bazaar_data):
    with open(CSVDownloadsPath + 'buy_summary.csv', 'w', newline='\n', encoding='utf-8') as foo:
        writer = csv.writer(foo)
        buySummaryArray = getBuySummaries(bazaar_data)
        for item in buySummaryArray:
            writer.writerow(item)


def read_buy_summary():
    with open(CSVDownloadsPath + 'buy_summary.csv') as csvDataFile:
        buy_summaries = dict()
        csvReader = csv.reader(csvDataFile)
        print('file opened')
        next(csvReader)
        for row in csvReader:
            product_id = row[0]
            buyOrder = BazaarBuySummary(id=enumerate(row),product_id=row[0], amount=row[1], pricePerUnit=row[2], orders=row[3])
            if product_id in buy_summaries.keys():
                buy_summaries.get(product_id).append(buyOrder)
            else:
                newArray = list()
                buy_summaries[product_id] = newArray
                print(product_id + ' was not in dict so it was added')
    return buy_summaries


def read_sell_summary():
    with open(CSVDownloadsPath + 'sell_summary.csv') as csvDataFile:
        sell_summaries = dict()
        csvReader = csv.reader(csvDataFile)
        print('file opened')
        next(csvReader)
        for row in csvReader:
            product_id = row[0]
            sellOrder = BazaarSellSummary(id=enumerate(row),product_id=row[0], amount=row[1], pricePerUnit=row[2], orders=row[3])
            if product_id in sell_summaries.keys():
                sell_summaries.get(product_id).append(sellOrder)
            else:
                newArray = list()
                sell_summaries[product_id] = newArray
                print(product_id + ' was not in dict so it was added')
    return sell_summaries


def read_quick_status():
    with open(CSVDownloadsPath + 'quick_status.csv') as csvDataFile:
        quick_statuses = dict()
        csvReader = csv.reader(csvDataFile)
        print('file opened')
        next(csvReader)
        for row in csvReader:
            product_id = row[0]
            quickStatus = BazaarQuickStatus(id=enumerate(row), product_id=product_id,sellPrice=row[1],sellVolume=row[2],
                                            sellMovingWeek=row[3],sellOrders=row[4],buyPrice=row[5],buyVolume=row[6],
                                            buyMovingWeek=row[7],buyOrders=row[8])
            quick_statuses[product_id] = quickStatus
            print(product_id + ' was not in dict so it was added')
    return quick_statuses


def write_bazaar_listing_file():
    buySummary = read_buy_summary()
    sellSummary = read_sell_summary()
    quickStatus = read_quick_status()
    finalArray = [['id', 'product_id', 'buy_summary', 'sell_summary', 'quick_status']]
    for item in buySummary:
        product_id = (buySummary[item][0]).product_id
        tempArray = [enumerate(buySummary[item]), product_id, buySummary[item], sellSummary[item], quickStatus[item]]
        finalArray.append(tempArray)
    with open(CSVDownloadsPath + 'bazaar_listing.csv', 'w', newline='\n', encoding='utf-8') as foo:
        writer = csv.writer(foo)
        writer.writerows(finalArray)


bazaarData = get_bazaar_data()
write_buy_summary_file(bazaar_data=bazaarData)
write_sell_summary_file(bazaar_data=bazaarData)
write_quick_status_file(bazaar_data=bazaarData)
write_bazaar_listing(bazaar_data=bazaarData)

conn = connect_to_SQLite()
update_bazaar_bazaarquickstatus_table(cursor=conn.cursor(), conn=conn)
update_bazaar_bazaarbuysummary_table(cursor=conn.cursor(), conn=conn)
update_bazaar_bazaarsellsummary_table(cursor=conn.cursor(), conn=conn)
update_bazaar_bazaarlisting_table(cursor=conn.cursor(), conn=conn)
print('Bazaar Scripts Ran.')


