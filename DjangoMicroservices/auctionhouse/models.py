from django.db import models


class AuctionListing(models.Model):
    item_name = models.CharField(max_length=1000, null=True)
    tier = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=50, null=True)
    auctioneer = models.CharField(max_length=128, null=True)
    starting_bid = models.FloatField()
    item_bytes = models.CharField(max_length=5000, null=True)
    count = models.IntegerField()
    username = models.CharField(max_length=32, null=True)
    start = models.CharField(max_length=50, null=True)
    end = models.CharField(max_length=50, null=True)
    bin = models.BooleanField(default=False, null=True)
    uuid = models.CharField(max_length=128, null=True)

