from django.conf import settings
from django.db import models
from colorfield.fields import ColorField
from dashboard_builders.constants import BUILDER_ITEM_CHART_TYPE_CHOICES, ChartType


class StockDashboardBuilderTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "stock_dashboard_builder_templates"
        verbose_name = "dashboard template"

    def __str__(self):
        return self.name


class StockDashboardBuilderItem(models.Model):
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(
        StockDashboardBuilderTemplate,
        on_delete=models.CASCADE,
        related_name="templates",
    )
    name = models.CharField(max_length=200)
    chart_type = models.PositiveSmallIntegerField(
        choices=BUILDER_ITEM_CHART_TYPE_CHOICES, default=ChartType.LINE
    )
    color = ColorField(default="#FF0000")
    label = models.CharField(max_length=50)

    class Meta:
        db_table = "stock_dashboard_builder_items"
        verbose_name = "dashboard builder item"
