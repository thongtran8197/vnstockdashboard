class ChartType:
    AREA = 1
    BAR = 2
    BUBBLE = 3
    DOUGHNUT_AND_PIE = 4
    LINE = 5
    MIXED = 6
    POLAR_AREA = 7
    RADAR = 8
    SCATTER = 9

    @classmethod
    def to_text(cls, chart_type: int) -> str:
        chart_type_text = ""
        if chart_type == cls.AREA:
            chart_type_text = "Area"
        elif chart_type == cls.BAR:
            chart_type_text = "Bar"
        elif chart_type == cls.BUBBLE:
            chart_type_text = "Bubble"
        elif chart_type == cls.DOUGHNUT_AND_PIE:
            chart_type_text = "Doughnut and Pie"
        elif chart_type == cls.LINE:
            chart_type_text = "Line"
        elif chart_type == cls.MIXED:
            chart_type_text = "Mixed"
        elif chart_type == cls.POLAR_AREA:
            chart_type_text = "Polar Area"
        elif chart_type == cls.POLAR_AREA:
            chart_type_text = "Polar Area"
        elif chart_type == cls.RADAR:
            chart_type_text = "Radar"
        elif chart_type == cls.SCATTER:
            chart_type_text = "Scatter"
        return chart_type_text


BUILDER_ITEM_CHART_TYPE_CHOICES = (
    (ChartType.BAR, ChartType.to_text(ChartType.BAR)),
    (ChartType.LINE, ChartType.to_text(ChartType.LINE)),
)


class ChartTimeUnit:
    DAY = 1
    MONTH = 2
    YEAR = 3
