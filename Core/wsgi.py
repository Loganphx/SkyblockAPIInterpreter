"""
WSGI config for Core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from PythonScripts.HypixelScrapingLibrary.Bazaar.bazaar_scripts import read_buy_summary, get_bazaar_data

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
bazaar_data = get_bazaar_data()
read_buy_summary(bazaar_data)
