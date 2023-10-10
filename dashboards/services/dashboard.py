from dashboard_builders.constants import ChartType
from dashboard_builders.models import StockDashboardBuilderTemplate


class DashboardService:
    @classmethod
    def get_builder_templates(cls, user_id: int) -> list:
        templates = []
        dashboard_templates = StockDashboardBuilderTemplate.objects.filter(
            added_by=user_id
        ).prefetch_related("templates")
        for dashboard_template in dashboard_templates:
            template = dict(name=dashboard_template.name)
            datasets = []
            for item in dashboard_template.templates.all():
                datasets.append(
                    dict(
                        type=ChartType.to_text(item.chart_type).lower(),
                        label=item.name,
                        data=[100, 150, 100, 180, 100, 112, 81, 329],
                        borderColor=item.color,
                        backgroundColor=item.color,
                    )
                )
            template.update(
                data=dict(datasets=datasets, labels=[1, 2, 4, 5, 6, 7, 8, 9])
            )
            template.update(options={})
            templates.append(template)
        return templates
