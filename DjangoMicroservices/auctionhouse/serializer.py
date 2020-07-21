from DjangoMicroservices.auctionhouse.models import AuctionListing
from rest_framework import serializers


class AuctionListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionListing
        fields = ['item_name', 'tier', 'category', 'auctioneer', 'starting_bid', 'count', 'start', 'end',
                  'bin', 'uuid', 'username', 'item_bytes']
