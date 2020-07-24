import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from DjangoMicroservices.auctionhouse.models import AuctionListing
from DjangoMicroservices.auctionhouse.serializer import AuctionListingSerializer


@api_view(['Get'])
def get_auction_item_name(request):
    query_set = AuctionListing.objects.values('item_name').distinct()
    json_data = json.dumps(list(query_set))
    return HttpResponse(json_data)
