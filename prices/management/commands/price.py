from django.core.management.base import BaseCommand
from vnstock import *

from prices.constants.price import (
    TimeRangeType,
    INCOME_STATEMENT_QUARTERLY_BAD_CODES,
    BALANCE_SHEET_YEARLY_BAD_CODES,
    BALANCE_SHEET_QUARTERLY_BAD_CODES,
    INSIDER_DEALS_MAPPING_METHOD,
    INSIDER_DEALS_MAPPING_ACTION,
)
from prices.models import IncomeStatement, FinancialRatio
from prices.models.price import BalanceSheet, InsiderDeals, FinancialFlow
from stocks.models import Stock


class Command(BaseCommand):
    help = "Crawl indicator of VN stock"

    def add_arguments(self, parser):
        parser.add_argument(
            "--crawl_income_statement",
            action="store_true",
            help="Crawl income statement",
        )
        parser.add_argument(
            "--crawl_financial_ratio",
            action="store_true",
            help="Crawl financial ratio",
        )
        parser.add_argument(
            "--crawl_balance_sheet",
            action="store_true",
            help="Crawl balance sheet",
        )
        parser.add_argument(
            "--stock_intraday_data",
            action="store_true",
            help="Crawl stock intraday data",
        )
        parser.add_argument(
            "--company_insider_deals",
            action="store_true",
            help="Crawl company insider deals",
        )
        parser.add_argument(
            "--financial_flows",
            action="store_true",
            help="Crawl financial flows",
        )

    def handle(self, *args, **options):
        if options.get("crawl_income_statement"):
            self.crawl_income_statement()
        elif options.get("crawl_financial_ratio"):
            self.crawl_financial_ratio()
        elif options.get("crawl_balance_sheet"):
            self.crawl_balance_sheet()
        elif options.get("stock_intraday_data"):
            self.stock_intraday_data()
        elif options.get("company_insider_deals"):
            self.company_insider_deals()
        elif options.get("financial_flows"):
            self.financial_flows()

    def crawl_income_statement(self):
        time_range_type = TimeRangeType.QUARTERLY
        bad_codes = INCOME_STATEMENT_QUARTERLY_BAD_CODES
        existed_codes = (
            IncomeStatement.objects.filter(time_range_type=time_range_type)
            .values_list("ticker", flat=True)
            .distinct()
        )
        stocks = (
            Stock.objects.exclude(code__in=existed_codes)
            .exclude(code__in=bad_codes)
            .values("id", "code")
        )
        for s in stocks:
            if len(s.get("code")) == 3:
                income_statements = financial_flow(
                    symbol=s.get("code"),
                    report_type="incomestatement",
                    report_range=TimeRangeType.to_text(time_range_type).lower(),
                )
                if income_statements:
                    bulk_create_income_statements = []
                    for i in income_statements:
                        bulk_create_income_statements.append(
                            IncomeStatement(
                                stock_id=s.get("id"),
                                ticker=i.get("ticker"),
                                time_range_type=time_range_type,
                                time_value="Q"
                                + str(i.get("quarter"))
                                + "-"
                                + str(i.get("year"))
                                if TimeRangeType.is_quarterly(time_range_type)
                                else i.get("year"),
                                revenue=i.get("revenue") or 0,
                                year_revenue_growth=i.get("yearRevenueGrowth") or 0,
                                quarter_revenue_growth=i.get("quarterRevenueGrowth")
                                or 0,
                                cost_of_good_sold=i.get("costOfGoodSold") or 0,
                                gross_profit=i.get("grossProfit") or 0,
                                operation_expense=i.get("operationExpense") or 0,
                                operation_profit=i.get("operationProfit") or 0,
                                year_operation_profit_growth=i.get(
                                    "yearOperationProfitGrowth"
                                )
                                or 0,
                                quarter_operation_profit_growth=i.get(
                                    "quarterOperationProfitGrowth"
                                )
                                or 0,
                                interest_expense=i.get("interestExpense") or 0,
                                pre_tax_profit=i.get("preTaxProfit") or 0,
                                post_tax_profit=i.get("postTaxProfit") or 0,
                                share_holder_income=i.get("shareHolderIncome") or 0,
                                year_share_holder_income_growth=i.get(
                                    "yearShareHolderIncomeGrowth"
                                )
                                or 0,
                                quarter_share_holder_income_growth=i.get(
                                    "quarterShareHolderIncomeGrowth"
                                )
                                or 0,
                                invest_profit=i.get("investProfit") or 0,
                                service_profit=i.get("serviceProfit") or 0,
                                other_profit=i.get("otherProfit") or 0,
                                provision_expense=i.get("provisionExpense") or 0,
                                operation_income=i.get("operationIncome") or 0,
                                ebitda=i.get("ebitda") or 0,
                            )
                        )
                    IncomeStatement.objects.bulk_create(bulk_create_income_statements)
                    self.stdout.write(f"Done {s.get('code')}")
                else:
                    self.stdout.write(f'"{s.get("code")}",')

    def crawl_financial_ratio(self):
        time_range_type = TimeRangeType.QUARTERLY
        ft = dict()
        if TimeRangeType.is_yearly(time_range_type):
            ft.update(quarter=0)
        elif TimeRangeType.is_quarterly(time_range_type):
            ft.update(quarter__gt=0)
        existed_codes = (
            FinancialRatio.objects.filter(**ft)
            .values_list("ticker", flat=True)
            .distinct()
        )
        bad_codes = []
        stocks = (
            Stock.objects.exclude(code__in=existed_codes)
            .exclude(code__in=bad_codes)
            .values("id", "code")
        )
        for s in stocks:
            if len(s.get("code")) == 3:
                financial_ratios = financial_ratio(
                    symbol=s.get("code"),
                    report_range=TimeRangeType.to_text(time_range_type).lower(),
                    is_all=True,
                )
                if financial_ratios:
                    bulk_create_financial_ratios = []
                    for f in financial_ratios:
                        bulk_create_financial_ratios.append(
                            FinancialRatio(
                                stock_id=s.get("id"),
                                ticker=f.get("ticker", ""),
                                quarter=f.get("quarter", "")
                                if TimeRangeType.is_quarterly(time_range_type)
                                else 0,
                                year=f.get("year", ""),
                                pe=f.get("priceToEarning") or 0,
                                pb=f.get("priceToBook") or 0,
                                roa=f.get("roa") or 0,
                                roe=f.get("roe") or 0,
                                eps=f.get("earningPerShare") or 0,
                                book_value_per_share=f.get("bookValuePerShare") or 0,
                                interest_margin=f.get("interestMargin") or 0,
                                non_interest_on_toi=f.get("nonInterestOnToi") or 0,
                                bad_debt_percentage=f.get("badDebtPercentage") or 0,
                                provision_on_bad_debt=f.get("provisionOnBadDebt") or 0,
                                cost_of_financing=f.get("costOfFinancing") or 0,
                                equity_on_total_asset=f.get("equityOnTotalAsset") or 0,
                                equity_on_loan=f.get("equityOnLoan") or 0,
                                cost_to_income=f.get("costToIncome") or 0,
                                equity_on_liability=f.get("equityOnLiability") or 0,
                                eps_change=f.get("epsChange") or 0,
                                asset_on_equity=f.get("assetOnEquity") or 0,
                                pre_provision_on_toi=f.get("preProvisionOnToi") or 0,
                                post_tax_on_toi=f.get("postTaxOnToi") or 0,
                                loan_on_earn_asset=f.get("loanOnEarnAsset") or 0,
                                loan_on_asset=f.get("loanOnAsset") or 0,
                                loan_on_deposit=f.get("loanOnDeposit") or 0,
                                deposit_on_earn_asset=f.get("depositOnEarnAsset") or 0,
                                bad_debt_on_asset=f.get("badDebtOnAsset") or 0,
                                liquidity_on_liability=f.get("liquidityOnLiability")
                                or 0,
                                payable_on_equity=f.get("payableOnEquity") or 0,
                                cancel_debt=f.get("cancelDebt") or 0,
                                book_value_per_share_change=f.get(
                                    "bookValuePerShareChange"
                                )
                                or 0,
                                credit_growth=f.get("creditGrowth") or 0,
                            )
                        )
                    FinancialRatio.objects.bulk_create(bulk_create_financial_ratios)
                    self.stdout.write(f"Done {s.get('code')}")
                else:
                    self.stdout.write(f'"{s.get("code")}",')

    def crawl_balance_sheet(self):
        time_range_type = TimeRangeType.YEARLY
        ft = dict()
        if TimeRangeType.is_yearly(time_range_type):
            ft.update(quarter=0)
        elif TimeRangeType.is_quarterly(time_range_type):
            ft.update(quarter__gt=0)
        existed_codes = (
            BalanceSheet.objects.filter(**ft)
            .values_list("ticker", flat=True)
            .distinct()
        )
        bad_codes = (
            BALANCE_SHEET_YEARLY_BAD_CODES
            if TimeRangeType.is_yearly(time_range_type)
            else BALANCE_SHEET_QUARTERLY_BAD_CODES
        )
        stocks = (
            Stock.objects.exclude(code__in=existed_codes)
            .exclude(code__in=bad_codes)
            .values("id", "code")
        )
        for s in stocks:
            if len(s.get("code")) == 3:
                balance_sheets = financial_flow(
                    symbol=s.get("code"),
                    report_type="balancesheet",
                    report_range=TimeRangeType.to_text(time_range_type).lower(),
                )
                if balance_sheets:
                    bulk_create_balance_sheets = []
                    for b in balance_sheets:
                        bulk_create_balance_sheets.append(
                            BalanceSheet(
                                stock_id=s.get("id"),
                                ticker=b.get("ticker", ""),
                                quarter=b.get("quarter", "")
                                if TimeRangeType.is_quarterly(time_range_type)
                                else 0,
                                year=b.get("year", ""),
                                short_asset=b.get("shortAsset", "") or 0,
                                cash=b.get("cash", "") or 0,
                                short_invest=b.get("shortInvest", "") or 0,
                                short_receivable=b.get("shortReceivable", "") or 0,
                                inventory=b.get("inventory", "") or 0,
                                long_asset=b.get("longAsset", "") or 0,
                                fixed_asset=b.get("fixedAsset", "") or 0,
                                asset=b.get("asset", "") or 0,
                                debt=b.get("debt", "") or 0,
                                short_debt=b.get("shortDebt", "") or 0,
                                long_debt=b.get("longDebt", "") or 0,
                                equity=b.get("equity", "") or 0,
                                capital=b.get("capital", "") or 0,
                                central_bank_deposit=b.get("centralBankDeposit", "")
                                or 0,
                                other_bank_deposit=b.get("otherBankDeposit", "") or 0,
                                other_bank_loan=b.get("otherBankLoan", "") or 0,
                                stock_invest=b.get("stockInvest", "") or 0,
                                customer_loan=b.get("customerLoan", "") or 0,
                                bad_load=b.get("badLoan", "") or 0,
                                provision=b.get("provision", "") or 0,
                                net_customer_loan=b.get("netCustomerLoan", "") or 0,
                                other_asset=b.get("otherAsset", "") or 0,
                                other_bank_credit=b.get("otherBankCredit", "") or 0,
                                owe_other_bank=b.get("oweOtherBank", "") or 0,
                                owe_central_bank=b.get("oweCentralBank", "") or 0,
                                valuable_paper=b.get("valuablePaper", "") or 0,
                                payable_interest=b.get("payableInterest", "") or 0,
                                receivable_interest=b.get("payableInterest", "") or 0,
                                deposit=b.get("deposit", "") or 0,
                                other_debt=b.get("otherDebt", "") or 0,
                                fund=b.get("fund", "") or 0,
                                un_distributed_income=b.get("unDistributedIncome", "")
                                or 0,
                                minor_share_holder_profit=b.get(
                                    "minorShareHolderProfit", ""
                                )
                                or 0,
                                payable=b.get("payable", "") or 0,
                            )
                        )
                    BalanceSheet.objects.bulk_create(bulk_create_balance_sheets)
                    self.stdout.write(f"Done {s.get('code')}")
                else:
                    self.stdout.write(f'"{s.get("code")}",')

    def stock_intraday_data(self):
        a = stock_intraday_data(symbol="TCB", page_size=200)
        a = 1

    def company_insider_deals(self):
        existed_codes = InsiderDeals.objects.values_list("ticker", flat=True).distinct()
        stocks = Stock.objects.exclude(code__in=existed_codes).values("id", "code")
        for s in stocks:
            bulk_create_insider_deals = []
            insider_deals = company_insider_deals(
                symbol=s.get("code"), page_size=1000, page=0
            ).get("listInsiderDealing", [])
            if insider_deals:
                for i in insider_deals:
                    bulk_create_insider_deals.append(
                        InsiderDeals(
                            stock_id=s.get("id"),
                            ticker=i.get("ticker", ""),
                            deal_announce_date=i.get("anDate", ""),
                            deal_method=INSIDER_DEALS_MAPPING_METHOD.get(
                                i.get("dealingMethod", ""), ""
                            ),
                            deal_action=INSIDER_DEALS_MAPPING_ACTION.get(
                                i.get("dealingAction", ""), ""
                            ),
                            deal_quantity=i.get("quantity", "") or 0,
                            deal_price=i.get("price", "") or 0,
                            deal_ratio=i.get("ratio", "") or 0,
                        )
                    )
                InsiderDeals.objects.bulk_create(
                    bulk_create_insider_deals, batch_size=200
                )
                self.stdout.write(f"Done {s.get('code')}")
            else:
                self.stdout.write(f'"{s.get("code")}",')

    def financial_flows(self):
        time_range_type = TimeRangeType.QUARTERLY
        ft = dict()
        if TimeRangeType.is_yearly(time_range_type):
            ft.update(quarter=0)
        elif TimeRangeType.is_quarterly(time_range_type):
            ft.update(quarter__gt=0)
        existed_codes = (
            FinancialFlow.objects.filter(**ft)
            .values_list("ticker", flat=True)
            .distinct()
        )
        stocks = Stock.objects.exclude(code__in=existed_codes).values("id", "code")
        for s in stocks:
            if len(s.get("code")) == 3:
                cash_flows = financial_flow(
                    symbol=s.get("code"),
                    report_type="cashflow",
                    report_range=TimeRangeType.to_text(time_range_type).lower(),
                )
                if cash_flows:
                    bulk_create_cash_flows = []
                    for c in cash_flows:
                        bulk_create_cash_flows.append(
                            FinancialFlow(
                                stock_id=s.get("id"),
                                ticker=c.get("ticker", ""),
                                quarter=c.get("quarter", "")
                                if TimeRangeType.is_quarterly(time_range_type)
                                else 0,
                                year=c.get("year", ""),
                                invest_code=c.get("investCost", "") or 0,
                                from_invest=c.get("fromInvest", "") or 0,
                                from_financial=c.get("fromFinancial", "") or 0,
                                from_sale=c.get("fromSale", "") or 0,
                                free_cash_flow=c.get("freeCashFlow", "") or 0,
                            )
                        )
                    FinancialFlow.objects.bulk_create(
                        bulk_create_cash_flows, batch_size=200
                    )
                    self.stdout.write(f"Done {s.get('code')}")
                else:
                    self.stdout.write(f'"{s.get("code")}",')
