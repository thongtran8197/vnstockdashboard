from datetime import datetime

from django.core.management import BaseCommand

from prices.constants.input_price import VN_BIZ_GOODS_URLS
from prices.services.input_price import InputPriceService


class Command(BaseCommand):
    help = "Crawl input prices"

    def add_arguments(self, parser):
        parser.add_argument(
            "--crawl_vn_biz_goods_price",
            action="store_true",
            help="Crawl vnbiz inout price",
        )

    def handle(self, *args, **options):
        if options.get("crawl_vn_biz_goods_price"):
            self.crawl_vn_biz_goods_price()

    def crawl_vn_biz_goods_price(self):
        from_date = datetime.strptime("2023-12-24", "%Y-%m-%d")
        for url in VN_BIZ_GOODS_URLS:
            InputPriceService.crawl_goods_price(good=url, from_date=from_date)
