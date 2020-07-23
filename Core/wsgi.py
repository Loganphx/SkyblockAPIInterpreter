"""
WSGI config for Core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import time
from asyncio.tasks import wait

from django.core.wsgi import get_wsgi_application

from PythonScripts.HypixelScrapingLibrary.AuctionHouse import auction_scripts
from PythonScripts.HypixelScrapingLibrary.AuctionHouse.auction_scripts import write_usernames_file, isUsernameInDict, \
    get_auction_bins
from PythonScripts.HypixelScrapingLibrary.Bazaar import bazaar_scripts
from PythonScripts.HypixelScrapingLibrary.Bazaar.bazaar_scripts import read_buy_summary, get_bazaar_data, \
    write_bazaar_listing, write_bazaar_listing_file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')

application = get_wsgi_application()

"""x = AuctionListing.objects.filter(item_name='Crystal Fragment')
serializer_data = AuctionListingSerializer(x, many=True)
for item in serializer_data.data[0:5]:
    print(item)

for item in x[0:5]:
    print(item.item_name)
    print(item.count)
    """
# bazaar_data = get_bazaar_data()
# print('Scripts started')
# bazaar_scripts
# auction_scripts
# i = 0
# while i != 1000:
#     isUsernameInDict(get_auction_bins())
#     i = i + 1
#     print('Program has ran ' + str(i) + ' times')
#     time.sleep(60)
