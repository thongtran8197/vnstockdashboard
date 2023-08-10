import csv
import os

from stocks.models import StockCategory, Stock
from vnstock import *


class StockService:
    @classmethod
    def import_vn_stock_category(cls):
        file_path = os.getcwd() + "/stocks/fixtures/stockcategory.csv"
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            stock_categories = []
            map_icb_code_lv1 = dict()
            map_icb_code_lv2 = dict()
            map_icb_code_lv3 = dict()
            StockCategory.objects.all().delete()
            for row in csv_reader:
                level = row[5]
                name = ""
                icb_code = row[0].zfill(4) if len(row[0]) < 4 else row[0]
                parent_id_level_1 = ""
                parent_id_level_2 = ""
                parent_id_level_3 = ""
                if level == "1":
                    name = row[1]
                    map_icb_code_lv1.update({row[1]: icb_code})
                elif level == "2":
                    name = row[2]
                    map_icb_code_lv2.update({row[2]: icb_code})
                    parent_id_level_1 = map_icb_code_lv1.get(row[1], "")
                elif level == "3":
                    name = row[3]
                    map_icb_code_lv3.update({row[3]: icb_code})
                    parent_id_level_1 = map_icb_code_lv1.get(row[1], "")
                    parent_id_level_2 = map_icb_code_lv2.get(row[2], "")
                elif level == "4":
                    name = row[4]
                    parent_id_level_1 = map_icb_code_lv1.get(row[1], "")
                    parent_id_level_2 = map_icb_code_lv2.get(row[2], "")
                    parent_id_level_3 = map_icb_code_lv3.get(row[3], "")
                stock_categories.append(
                    StockCategory(
                        icb_code=icb_code,
                        name=name,
                        level=level,
                        parent_id_level_1=parent_id_level_1,
                        parent_id_level_2=parent_id_level_2,
                        parent_id_level_3=parent_id_level_3,
                    )
                )
            StockCategory.objects.bulk_create(stock_categories)

    @classmethod
    def import_vn_stock(cls):
        file_path = os.getcwd() + "/stocks/fixtures/stocks.csv"
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            categories = StockCategory.objects.values("icb_code", "id")
            categories_map = {}
            [
                categories_map.update({c.get("icb_code"): c.get("id")})
                for c in categories
            ]
            Stock.objects.all().delete()
            for row in csv_reader:
                stock = Stock(
                    code=row[0],
                    name=row[1],
                    category_id=categories_map.get(
                        row[2].zfill(4) if len(row[2]) < 4 else row[2]
                    ),
                )
                stock.save()

    @classmethod
    def get_stock_dividend_history(cls, stock_code: str):
        try:
            history = dividend_history(stock_code)
            return history
        except Exception:
            return None

    @classmethod
    def get_stock_historical_data(
        self, stock_code: str, start_date: str, end_date: str
    ):
        try:
            historical_data = stock_historical_data(
                symbol=stock_code,
                start_date=start_date,
                end_date=end_date,
                resolution="1D",
                type="stock",
            )
            return historical_data
        except Exception:
            return None
