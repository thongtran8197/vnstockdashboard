from django.db import models


class StockCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    icb_code = models.CharField(max_length=4)
    parent_id_level_1 = models.CharField(max_length=4)
    parent_id_level_2 = models.CharField(max_length=4)
    parent_id_level_3 = models.CharField(max_length=4)
    level = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "vn_stock_categories"


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=500)
    category = models.ForeignKey(
        StockCategory, on_delete=models.CASCADE, related_name="stocks"
    )

    class Meta:
        db_table = "vn_stocks"


class StockDividendHistory(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, db_index=True)
    exercise_date = models.DateTimeField()
    cash_year = models.PositiveSmallIntegerField()
    cash_dividend_percentage = models.FloatField()
    issue_method = models.CharField(max_length=20)

    class Meta:
        db_table = "vn_stock_dividend_histories"
        verbose_name = "dividend historie"


class StockHistorical(models.Model):
    """Price by day"""

    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock_historical"
    )
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()

    class Meta:
        db_table = "vn_stock_historical_data"
