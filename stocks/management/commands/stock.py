import datetime

from django.core.management.base import BaseCommand

from stocks.models import Stock, StockDividendHistory
from stocks.services.stock import StockService


class Command(BaseCommand):
    help = "Import VN Stock Code"

    def add_arguments(self, parser):
        parser.add_argument("--import_vn_stock_category", action="store_true", help="Import VN stock category")
        parser.add_argument("--import_vn_stock", action="store_true", help="Import VN stock")
        parser.add_argument("--get_stock_dividend_history", action="store_true", help="Get stock dividend history")

    def handle(self, *args, **options):
        if options.get("import_vn_stock_category"):
            self.import_vn_stock_category()
        elif options.get("import_vn_stock"):
            self.import_vn_stock()
        elif options.get("get_stock_dividend_history"):
            self.get_stock_dividend_history()

    def import_vn_stock_category(self):
        StockService.import_vn_stock_category()
        self.stdout.write("success")

    def import_vn_stock(self):
        StockService.import_vn_stock()
        self.stdout.write("success")

    def prepare_exercise_date(self, exercise_date: str) -> str:
        date_array = exercise_date.split("/")
        formatted_exercise_date = "20" + date_array[2] + "-" + date_array[1] + "-" + date_array[0]
        return formatted_exercise_date

    def get_stock_dividend_history(self):
        stocks = Stock.objects.values_list("code", flat=True)
        # stocks = ['TTA']
        for stock in stocks:
            histories = StockService.get_stock_dividend_history(stock)
            if histories is not None:
                history_data = []
                for history in histories.values:
                    history_data.append(
                        StockDividendHistory(
                            code=stock,
                            exercise_date=self.prepare_exercise_date(history[0]),
                            cash_year=history[1],
                            cash_dividend_percentage=history[2],
                            issue_method=history[3]
                        )
                    )
                StockDividendHistory.objects.bulk_create(history_data, batch_size=500)
                self.stdout.write(f"Done {stock}")

