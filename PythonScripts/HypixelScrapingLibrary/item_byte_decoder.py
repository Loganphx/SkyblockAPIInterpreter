import nbt
import io
import base64
import requests


def decode_item_bytes(item_bytes):
    data = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(item_bytes)))
    return data.pretty_tree()


def get_count(data):
    count = data['i'][0]['Count']
    return count
