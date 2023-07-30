from rest_framework.response import Response
from rest_framework import viewsets, status

from stocks.models import Stock
from stocks.serializers import StockSerializer


class StockViewSet(viewsets.ViewSet):
    serializer_class = StockSerializer

    def list(self, request):
        stocks = Stock.objects.order_by("id").all()
        stocks_data = StockSerializer(stocks, many=True).data
        return Response(stocks_data, status=status.HTTP_200_OK)

