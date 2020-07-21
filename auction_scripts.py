import json
import requests
import time
import csv

from item_byte_decoder import decode_item_bytes, get_count


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
    return(auction_items)
    print(end_time - start_time)

def get_username(uuid):
    x = requests.get('https://playerdb.co/api/player/minecraft/' + str(uuid))
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    return json_loaded['data']['player']['username']
get_username("576976155b5b4730bdaf5f74ff3ab20d")

def parse_auction_listings(auction_data):
    final_array = []
    for item in auction_data:
        passing_array = []
        passing_array.append(item['item_name'])
        passing_array.append(item['tier'])
        passing_array.append(item['category'])
        passing_array.append(get_username([item['auctioneer']]))
        passing_array.append(item['starting_bid'])
        item_data = decode_item_bytes(item['item_bytes'])
        passing_array.append(get_count(item_data))
        passing_array.append(item['auctioneer'])
        passing_array.append(item['start'])
        passing_array.append(item['end'])
        passing_array.append(item['bin'])
        passing_array.append(item['uuid'])
        passing_array.append(item['item_bytes'])

        final_array.append(passing_array)

        return final_array

def write_auctions_file(auctions_array):
    with open('test.csv', 'w', newline='\n', encoding='utf-8') as auc:
        writer = csv.writer(auc)
        writer.writerows(auctions_array)


