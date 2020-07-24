from DjangoMicroservices.auctionhouse.models import AuctionListing
from rest_framework import serializers


class AuctionListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionListing
        fields = ['item_name', 'tier', 'category', 'auctioneer', 'starting_bid', 'item_bytes', 'count', 'username', 'start', 'end',
                  'bin', 'uuid']
