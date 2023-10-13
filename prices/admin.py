import csv

from django.contrib import admin
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter

from prices.constants.input_price import VN_BIZ_GOODS_URLS, VnBizGoodsUrlTypeMapping
from prices.models import InputPrice
from rangefilter.filters import DateRangeFilterBuilder

from vnstockdashboard.mixin import ExportCsvMixin


class InputPriceFilterType(MultipleChoiceListFilter):
    title = "Type"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        # generate the list of choices
        types = []
        for url in VN_BIZ_GOODS_URLS:
            types.append((VnBizGoodsUrlTypeMapping.get(url), f"{VnBizGoodsUrlTypeMapping.get(url)} - {url}"))
        return types

    def queryset(self, request, queryset):
        # filter the queryset by the selected value
        value = self.value()
        if value is not None:
            types = [int(v) for v in self.value().split(",")]
            ft = dict(type__in=types)
            return queryset.filter(**ft)
        return queryset


# Register your models here.
@admin.register(InputPrice)
class InputPriceAdmin(admin.ModelAdmin):
    list_display = ("type", "date", "value", "unit")
    list_filter = (
        ("date", DateRangeFilterBuilder()),
        InputPriceFilterType,
    )
    ordering = ("type", "-date")
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        file_name = "hang_hoa"
        field_names = ["date", "year", "month", "day", "value", "unit", "type"]
        response = ExportCsvMixin.export_as_csv(
            queryset,
            **dict(
                file_name=file_name,
                field_names=field_names
            )
        )
        return response

    export_as_csv.short_description = "Export Selected"
