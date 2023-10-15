from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from dashboards.services.input_price_dashboard import InputPriceDashboardService


# Create your views here.
@staff_member_required
def input_price_chart(request):
    data = request.GET.copy()
    input_price_type = int(data.get("input_price_type"), 0)
    input_price_chart = InputPriceDashboardService.get_chart_data_by_type(
        input_price_type
    )
    return JsonResponse({"data": input_price_chart})
