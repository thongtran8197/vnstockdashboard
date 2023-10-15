import json

from django.contrib import admin
from dashboards.models import FakeDashboard
from dashboards.services.dashboard import DashboardService
from dashboards.services.input_price_dashboard import InputPriceDashboardService
from prices.constants.input_price import VnBizGoodsUrlTypeMapping


class Dashboarad(FakeDashboard):
    class Meta:
        proxy = True
        verbose_name = "Dashboard"


@admin.register(Dashboarad)
class DashboardAdmin(admin.ModelAdmin):
    change_list_template = "admin/dashboard.html"

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        chart_templates = DashboardService.get_builder_templates(
            user_id=request.user.id
        )
        extra_context = extra_context or {"chart_templates": chart_templates}
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class InputPriceDashboard(FakeDashboard):
    class Meta:
        proxy = True
        verbose_name = "Input Price Dashboard"


@admin.register(InputPriceDashboard)
class InputPriceDashboardAdmin(admin.ModelAdmin):
    change_list_template = "admin/input_price_dashboard.html"

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        chart_data = InputPriceDashboardService.get_chart_data_by_type(
            input_price_type=VnBizGoodsUrlTypeMapping.get("lon_hoi_trung_quoc")
        )
        extra_context = extra_context or {"chart_data": chart_data}
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
