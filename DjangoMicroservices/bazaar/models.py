from django.db import models


# Create your models here.

class BazaarBuySummary(models.Model):
    product_id = models.CharField(max_length=1000, null=True)
    amount = models.IntegerField()
    pricePerUnit = models.FloatField()
    orders = models.IntegerField()


class BazaarSellSummary(models.Model):
    product_id = models.CharField(max_length=1000, null=True)
    amount = models.IntegerField()
    pricePerUnit = models.FloatField()
    orders = models.IntegerField()


class BazaarQuickStatus(models.Model):
    product_id = models.CharField(max_length=1000, null=True)
    sellPrice = models.FloatField()
    sellVolume = models.IntegerField()
    sellMovingWeek = models.IntegerField()
    sellOrders = models.IntegerField()
    buyPrice = models.FloatField()
    buyVolume = models.IntegerField()
    buyMovingWeek = models.IntegerField()
    buyOrders = models.IntegerField()


class BazaarListing(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    buy_summary = models.OneToOneField(BazaarBuySummary, on_delete=models.CASCADE)
    sell_summary = models.OneToOneField(BazaarSellSummary, on_delete=models.CASCADE)
    quick_status = models.OneToOneField(BazaarQuickStatus, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id', 'buy_summary', 'sell_summary', 'quick_status']
