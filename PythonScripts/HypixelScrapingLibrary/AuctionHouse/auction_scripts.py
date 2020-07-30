import base64
import io
import json
import requests
import time
import csv
import nbt

from Core.settings import CSVDownloadsPath, APIKEY
from PythonScripts.SQLiteLibrary.SQLiteConnection import update_auction_listings_table, connect_to_SQLite


def get_auction_bins() -> json:
    start_time = time.time()
    URL = 'https://api.hypixel.net/skyblock/auctions?key=' + APIKEY
    x = requests.get(URL)
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    total_Pages = json_loaded['totalPages']
    page = 0
    auction_items = []
    for page in range(total_Pages):
        x = requests.get(URL + '&page=' + str(page))
        print(x)
        parsed = json.dumps(x.json())
        json_loaded = json.loads(parsed)
        for listing in json_loaded['auctions']:
            if ('bin' in listing.keys()):
                if (listing['bin'] == True):
                    auction_items.append(listing)

    end_time = time.time()
    print(end_time - start_time)
    return (auction_items)


def get_username(uuid):
    x = requests.get('https://playerdb.co/api/player/minecraft/' + str(uuid))
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    return json_loaded


def parse_auction_listings(auction_data):
    final_array = [
        ['item_name', 'tier', 'category', 'starting_bid', 'count', 'auctioneer', 'start', 'end', 'bin', 'uuid',
         'item_bytes']]
    usernameDict = read_username_dict()
    for item in auction_data:
        passing_array = []
        passing_array.append(item['item_name'])
        passing_array.append(item['tier'])
        passing_array.append(item['category'])
       # passing_array.append(usernameDict[item['username']])
        passing_array.append(item['starting_bid'])
        data = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(item['item_bytes'])))
        count = data['i'][0]['Count']
        passing_array.append(count)
        passing_array.append(item['auctioneer'])
        passing_array.append(item['start'])
        passing_array.append(item['end'])
        passing_array.append(item['bin'])
        passing_array.append(item['uuid'])
        passing_array.append(item['item_bytes'])
        final_array.append(passing_array)
    print('Done')
    return final_array


def write_auctions_file(auctions_array):
    with open(CSVDownloadsPath + 'auction_data.csv', 'w', newline='\n', encoding='utf-8') as foo:
        writer = csv.writer(foo)
        writer.writerows(auctions_array)


def read_username_dict():
    with open(CSVDownloadsPath + 'username_dict.csv') as csvDataFile:
        username_dict = dict()
        csvReader = csv.reader(csvDataFile)
        print('file opened')
        for row in csvReader:
            userid = row[0]
            if ((userid in username_dict.keys()) != True):
                username_dict[userid] = row[1]
    return username_dict


def write_usernames_file(userid, username):
    with open(CSVDownloadsPath + 'username_dict.csv', 'a', newline='\n', encoding='utf-8') as foo:
        writer = csv.writer(foo)
        myarray = [userid, username]
        writer.writerow(myarray)


def isUsernameInDict(auctions_data):
    usernameDatabase = read_username_dict()
    for item in auctions_data:
        userid = item['auctioneer']
        if not (userid in usernameDatabase.keys()):
            x = requests.get('https://playerdb.co/api/player/minecraft/' + userid)
            parsed = json.dumps(x.json())
            json_loaded = json.loads(parsed)
            username = json_loaded['data']['player']['username']
            usernameDatabase[userid] = username

            write_usernames_file(userid, username)


'''
auction_data = get_auction_bins()
isUsernameInDict(auction_data)
auctions_array = parse_auction_listings(auction_data)
write_auctions_file(auctions_array)
conn = connect_to_SQLite()
update_auction_listings_table(cursor=conn.cursor(), conn=conn)
print('Auction Scripts Ran.')
'''
'''
# How to query using the ORM. Call model classes like AuctionListing
x = AuctionListing.objects.filter(item_name='Crystal Fragment')
for item in x[0:5]:
    # Item attributes are called with .attributeName
    print(item.item_name)
    print(item.count)

gi

# How to serialize a query_set that is returned by Django ORM
serializer_data = AuctionListingSerializer(x, many=True)
for item in serializer_data.data[0:5]:
    # items become ordered dictionaries. To remove order use dict(ordered_dict)
    print(item)

'''
