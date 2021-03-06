from django.db import models


# Create your models here.

class BazaarBuySummary(models.Model):
    product_id = models.CharField(max_length=1000)
    amount = models.IntegerField()
    pricePerUnit = models.FloatField()
    orders = models.IntegerField()


class BazaarSellSummary(models.Model):
    product_id = models.CharField(max_length=1000)
    amount = models.IntegerField()
    pricePerUnit = models.FloatField()
    orders = models.IntegerField()


class BazaarQuickStatus(models.Model):
    product_id = models.CharField(max_length=1000, primary_key=True)
    sellPrice = models.FloatField()
    sellVolume = models.IntegerField()
    sellMovingWeek = models.IntegerField()
    sellOrders = models.IntegerField()
    buyPrice = models.FloatField()
    buyVolume = models.IntegerField()
    buyMovingWeek = models.IntegerField()
    buyOrders = models.IntegerField()


class BazaarListing(models.Model):
    product_id = models.CharField(max_length=1000, primary_key=True)
    buy_summary = models.ForeignKey(BazaarBuySummary, on_delete=models.CASCADE)
    sell_summary = models.ForeignKey(BazaarSellSummary, on_delete=models.CASCADE)
    quick_status = models.ForeignKey(BazaarQuickStatus, on_delete=models.CASCADE)

    '''class Meta:
        ordering = ['product_id', 'buy_summary', 'sell_summary', 'quick_status']
    '''