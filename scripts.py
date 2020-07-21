import json
import requests

def get_bazaar_data() -> json:
    x = requests.get('https://api.hypixel.net/skyblock/bazaar?key=41b2a888-f84c-4287-bf56-2012895c8e4d')
    parsed = json.dumps(x.json())
    json_loaded = json.loads(parsed)
    return json_loaded


def get_item_sells(item: str, howMany: int, jsonLoaded: json) -> []:
    stringArray = []
    for k in jsonLoaded:
        if k == item.upper():
            sells = {k: v for k, v in sorted(jsonLoaded[k].items(), reverse=False, key=lambda item: len(item[1]))}
            sells = sells['sell_summary']
    for c, _object in enumerate(sells):
        passing_object = {'amount': _object['amount'],
                          'pricePerUnit': _object['pricePerUnit'],
                          'ordersNum': _object['orders'],
                          'index': c + 1,
                          'item_name': item
                          }
        stringArray.append(passing_object)
    return stringArray


def get_item_buys(item: str, howMany: int, jsonLoaded: json) -> []:
    stringArray = []
    for k in jsonLoaded:
        if k == item.upper():
            buys = {k: v for k, v in sorted(jsonLoaded[k].items(), reverse=False, key=lambda item: len(item[1]))}
            buys = buys['buy_summary']
            # print('BUY ORDERS' + '\n' + str(buys))
    for c, _object in enumerate(buys):
        cnt = len(buys) - c - 1
        _object = buys[cnt]
        passing_object = {'amount': _object['amount'],
                          'pricePerUnit': _object['pricePerUnit'],
                          'ordersNum': _object['orders'],
                          'index': cnt
                          }
        stringArray.append(passing_object)
    return stringArray