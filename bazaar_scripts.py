import json
import requests

from item_byte_decoder import decode_item_bytes, get_count


def get_bazaar_data() -> json:
    x = requests.get('https://api.hypixel.net/skyblock/bazaar?key=41b2a888-f84c-4287-bf56-2012895c8e4d')
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    return json_loaded

def get_sell_summary(bazaar):
    bazaar = get_bazaar_data()
    for item in bazaar['products']:
        print(item)
        for info in bazaar['products'][item]['sell_summary']:
            print(info)

def get_buy_summary(bazaar):
    #bazaar = get_bazaar_data()
    for item in bazaar['products']:
        print(item)
        for info in bazaar['products'][item]['buy_summary']:
            print(info)

def get_quick_status(bazaar):
    for item in bazaar['products']:
        print('\n' + item)
        for status in bazaar['products'][item]['quick_status']:
            print(status + ' , ' + str(bazaar['products'][item]['quick_status'][status]))

def parse_bazaar_listings(bazaar_data):
    final_array = []
    for item in bazaar_data:
        passing_array = []
        passing_array.append(get_sell_summary(bazaar_data))
        passing_array.append(get_buy_summary(bazaar_data))
        passing_array.append(get_quick_status(bazaar_data))

        final_array.append(passing_array)

        return final_array