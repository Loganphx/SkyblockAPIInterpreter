from django.urls import path
from . import views

app_name = 'auctionhouse'

urlpatterns = [
    path('auctionhouse/get_item_names', views.get_auction_item_name, name='REST API get Auction names'),
]
