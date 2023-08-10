from django.contrib import admin
from dashboard_builders.models import (
    StockDashboardBuilderTemplate,
    StockDashboardBuilderItem,
)
from related_admin import RelatedFieldAdmin


@admin.register(StockDashboardBuilderTemplate)
class StockDashboardBuilderTemplateAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]


@admin.register(StockDashboardBuilderItem)
class StockDashboardBuilderItemAdmin(RelatedFieldAdmin):
    list_display = ("name", "template__name")
    search_fields = ["name", "template__name"]
    autocomplete_fields = ["template"]
