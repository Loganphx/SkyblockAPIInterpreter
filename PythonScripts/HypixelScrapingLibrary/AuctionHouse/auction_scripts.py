import base64
import io
import json
import requests
import time
import csv
import nbt

from Core.settings import CSVDownloadsPath
from DjangoMicroservices.auctionhouse.models import AuctionListing
from DjangoMicroservices.auctionhouse.serializer import AuctionListingSerializer


def get_auction_bins() -> json:
    start_time = time.time()
    x = requests.get('https://api.hypixel.net/skyblock/auctions?key=41b2a888-f84c-4287-bf56-2012895c8e4d')
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    total_Pages = json_loaded['totalPages']
    page = 0
    auction_items = []
    while(page < total_Pages):
        x = requests.get('https://api.hypixel.net/skyblock/auctions?key=41b2a888-f84c-4287-bf56-2012895c8e4d&page=' + str(page))
        parsed = json.dumps(x.json())
        json_loaded = json.loads(parsed)
        for listing in json_loaded['auctions']:
            if('bin' in listing.keys()):
                if(listing['bin'] == True):
                    auction_items.append(listing)
        page=page+1

    end_time = time.time()
    print(end_time - start_time)
    return(auction_items)


def get_username(uuid):
    x = requests.get('https://playerdb.co/api/player/minecraft/' + str(uuid))
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    return json_loaded


def parse_auction_listings(auction_data):
    final_array = [['item_name', 'tier', 'category', 'starting_bid', 'count', 'auctioneer', 'start', 'end', 'bin', 'uuid']]
    for item in auction_data:
        passing_array = []
        passing_array.append(item['item_name'])
        passing_array.append(item['tier'])
        passing_array.append(item['category'])
        #userid = item['auctioneer']
        #x = requests.get('https://playerdb.co/api/player/minecraft/' + userid)
        #parsed = json.dumps(x.json())
        #json_loaded = json.loads(parsed)
        #passing_array.append(json_loaded['data']['player']['username'])
        passing_array.append(item['starting_bid'])
        data = nbt.nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(item['item_bytes'])))
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


'''start_time = time.time()

auction_data = get_auction_bins()

auctions_array = parse_auction_listings(auction_data)

write_auctions_file(auctions_array)

cursor = connect_to_SQLite()

update_auction_listings_table(cursor=cursor)

end_time = time.time()
print(end_time - start_time)

# How to query using the ORM. Call model classes like AuctionListing
x = AuctionListing.objects.filter(item_name='Crystal Fragment')
for item in x[0:5]:
    # Item attributes are called with .attributeName
    print(item.item_name)
    print(item.count)


# How to serialize a query_set that is returned by Django ORM
serializer_data = AuctionListingSerializer(x, many=True)
for item in serializer_data.data[0:5]:
    # items become ordered dictionaries. To remove order use dict(ordered_dict)
    print(item)

'''