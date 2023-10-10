from django.conf import settings

from prices.models import InputPrice
import datetime


def crawl_input_price():
    a = InputPrice(
        date=datetime.date.today(),
        day=12,
        month=4,
        year=2023,
        type=1,
        unit="VND",
        value=1.2,
    )
    a.save()
    slack_data = dict(
        attachments=[
            dict(
                color="#ff4d46",
                mrkdwn_in=["text"],
                pretext=f"Input Price {str(datetime.date.today())}",
                title="Input Price Alert",
                text="test message",
            )
        ]
    )
    import requests

    requests.post(
        settings.SLACK_CRAWL_INPUT_GOODS_PRICE_WEBHOOK,
        headers={"Content-Type": "application/json"},
        json=slack_data,
    )


# Crawl VnBiz Goods
def crawl_vnbiz_goods():
    domain_url = (
        f"https://api.wichart.vn/vietnambiz/vi-mo?key=hang_hoa&to=2023-09-23&{good_url}"
    )
    pass
