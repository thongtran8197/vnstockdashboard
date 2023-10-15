from dashboard_builders.constants import ChartType
from prices.constants.input_price import (
    VnBizGoodsUrlTypeMapping,
    ReverseVnBizGoodsUrlTypeMapping,
)
from prices.models import InputPrice


class InputPriceDashboardService:
    @classmethod
    def get_chart_data_by_type(cls, input_price_type: int) -> dict:
        chart_data = (
            InputPrice.objects.filter(type=input_price_type)
            .exclude(value=0)
            .order_by("date")
        )
        labels = []
        data = []
        unit = chart_data[0].unit if chart_data else ""
        for d in chart_data:
            labels.append(str(d.date))
            data.append(d.value)
        return dict(
            data=dict(
                labels=labels,
                datasets=[
                    dict(
                        type=ChartType.to_text(ChartType.LINE).lower(),
                        label=ReverseVnBizGoodsUrlTypeMapping.get(input_price_type, "")
                        + " ("
                        + unit
                        + ")",
                        data=data,
                        borderColor="#79aec8",
                        backgroundColor="#79aec8",
                    )
                ],
            ),
            options=dict(scales=dict(y=dict(min=0))),
        )
