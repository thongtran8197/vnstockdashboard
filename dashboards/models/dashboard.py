from django.db import models


class StockDashboard(models.Model):
    id = models.AutoField(primary_key=True)
    fake_name = models.CharField(max_length=1)

    class Meta:
        db_table = "stock_dashboards"
        verbose_name = "dashboard"