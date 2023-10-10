from django.db import models


class InputPrice(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default="")
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    type = models.PositiveSmallIntegerField(db_index=True)
    unit = models.CharField(max_length=100)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "input_prices"
