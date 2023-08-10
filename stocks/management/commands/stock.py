import datetime

from django.core.management.base import BaseCommand

from stocks.models import Stock, StockDividendHistory
from stocks.models.stock import StockHistorical
from stocks.services.stock import StockService


class Command(BaseCommand):
    help = "Import VN Stock Code"

    def add_arguments(self, parser):
        parser.add_argument(
            "--import_vn_stock_category",
            action="store_true",
            help="Import VN stock category",
        )
        parser.add_argument(
            "--import_vn_stock", action="store_true", help="Import VN stock"
        )
        parser.add_argument(
            "--get_stock_dividend_history",
            action="store_true",
            help="Get stock dividend history",
        )
        parser.add_argument(
            "--get_stock_historical_data",
            action="store_true",
            help="Get stock historical data",
        )

    def handle(self, *args, **options):
        if options.get("import_vn_stock_category"):
            self.import_vn_stock_category()
        elif options.get("import_vn_stock"):
            self.import_vn_stock()
        elif options.get("get_stock_dividend_history"):
            self.get_stock_dividend_history()
        elif options.get("get_stock_historical_data"):
            self.get_stock_historical_data()

    def import_vn_stock_category(self):
        StockService.import_vn_stock_category()
        self.stdout.write("success")

    def import_vn_stock(self):
        StockService.import_vn_stock()
        self.stdout.write("success")

    def prepare_exercise_date(self, exercise_date: str) -> str:
        date_array = exercise_date.split("/")
        formatted_exercise_date = (
            "20" + date_array[2] + "-" + date_array[1] + "-" + date_array[0]
        )
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
                            issue_method=history[3],
                        )
                    )
                StockDividendHistory.objects.bulk_create(history_data, batch_size=500)
                self.stdout.write(f"Done {stock}")

    def get_stock_historical_data(self):
        start_date_str = "2012-03-20"
        end_date_obj = datetime.date.today()
        end_date_str = end_date_obj.strftime("%Y-%m-%d")
        stocks = Stock.objects.filter(code="HPG").values("code", "id")
        stock_mapping = dict()
        stock_codes = []
        for stock in stocks:
            stock_codes.append(stock.get("code", ""))
            stock_mapping.update({stock.get("code", ""): stock.get("id", 0)})
        for stock_code in stock_codes:
            historical_data = StockService.get_stock_historical_data(
                stock_code, start_date_str, end_date_str
            )
            if historical_data is not None:
                bulk_create_stock_historical = []
                for data in historical_data.values:
                    bulk_create_stock_historical.append(
                        StockHistorical(
                            stock_id=stock_mapping.get(stock_code),
                            date=data[0],
                            open=data[1],
                            high=data[2],
                            low=data[3],
                            close=data[4],
                            volume=data[5],
                        )
                    )
                StockHistorical.objects.bulk_create(
                    bulk_create_stock_historical, batch_size=500
                )
                self.stdout.write(f"Done {stock_code}")
