from datetime import datetime

from django.core.management import BaseCommand

from prices.constants.input_price import VN_BIZ_GOODS_URLS
from prices.models import InputPrice
from prices.services.input_price import InputPriceService


class Command(BaseCommand):
    help = "Crawl input prices"

    def add_arguments(self, parser):
        parser.add_argument(
            "--crawl_vn_biz_goods_price",
            action="store_true",
            help="Crawl vnbiz inout price",
        )
        parser.add_argument(
            "--correct_input_price_unit",
            action="store_true",
            help="correct input price unit",
        )

    def handle(self, *args, **options):
        if options.get("crawl_vn_biz_goods_price"):
            self.crawl_vn_biz_goods_price()
        elif options.get("correct_input_price_unit"):
            self.correct_input_price_unit()

    def crawl_vn_biz_goods_price(self):
        from_date = datetime.strptime("2023-11-17", "%Y-%m-%d")
        for url in VN_BIZ_GOODS_URLS:
            InputPriceService.crawl_goods_price(good=url, from_date=from_date)

    def correct_input_price_unit(self):
        input_prices = InputPrice.objects.all()
        bulk_create_input_prices = []
        for input_price in input_prices:
            input_price.unit = InputPriceService.convert_vietnamese(input_price.unit)
            bulk_create_input_prices.append(input_price)
        InputPrice.objects.bulk_update(bulk_create_input_prices, fields=["unit"], batch_size=5000)
