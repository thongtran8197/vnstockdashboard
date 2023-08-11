import json

from django.contrib import admin

from dashboard_builders.models import StockDashboardBuilderTemplate
from dashboards.models import FakeDashboard


@admin.register(FakeDashboard)
class FakeDashboardAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        chart_templates = StockDashboardBuilderTemplate.objects.filter(
            added_by=request.user.id
        )
        data = {
            "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
            "datasets": [
                {
                    "label": "My First Dataset",
                    "data": [65, 59, 80, 81, 56, 55, 0, 40],
                    "fill": False,
                    "borderColor": "rgb(75, 192, 192)",
                    "tension": 0.1,
                }
            ],
        }
        chart_data = {
            "type": "bar",
            "data": data,
        }
        extra_context = extra_context or {"chart_data": json.dumps(chart_data)}
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
