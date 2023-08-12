import json

from django.contrib import admin

from dashboard_builders.models import StockDashboardBuilderTemplate
from dashboards.models import FakeDashboard
from dashboards.services.dashboard import DashboardService


@admin.register(FakeDashboard)
class FakeDashboardAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        chart_templates = DashboardService.get_builder_templates(user_id=request.user.id)
        extra_context = extra_context or {"chart_templates": chart_templates}
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
