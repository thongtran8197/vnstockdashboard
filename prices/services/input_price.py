import datetime
import json

import requests

from prices.constants.input_price import VnBizGoodsUrlTypeMapping
from prices.models import InputPrice


class InputPriceService:
    domain_url = "https://api.wichart.vn/vietnambiz/vi-mo?"

    @classmethod
    def crawl_goods_price(cls, good: str, from_date):
        today = str(datetime.date.today())
        request_url = cls.domain_url + "key=hang_hoa&" + f"name={good}&to={today}"
        response = requests.get(url=request_url)
        if response.status_code == 200:
            data = json.loads(response.text)
            chart_data = data.get("chart", {})
            series_data = chart_data.get("series", [])
            if series_data:
                unit = series_data[0].get("unit", "")
                input_price_data = series_data[0].get("data", [])
                bulk_create_input_prices = []
                type = VnBizGoodsUrlTypeMapping.get(good, 0)
                for v in input_price_data:
                    date = datetime.datetime.fromtimestamp(v[0] / 1000)
                    # Extract year, month, and day from the integer
                    if date > from_date:
                        bulk_create_input_prices.append(
                            InputPrice(
                                date=date,
                                year=date.year,
                                month=date.month,
                                day=date.day,
                                type=type,
                                unit=unit,
                                value=v[1] or 0,
                            )
                        )
                InputPrice.objects.bulk_create(bulk_create_input_prices, batch_size=500)
