from rest_framework import serializers

from stocks.models import Stock


class StockSerializer(serializers.ModelSerializer):
    icb_code = serializers.CharField(read_only=True, source="category.icb_code")

    class Meta:
        model = Stock
        fields = ('id', "code", "name", "icb_code")
