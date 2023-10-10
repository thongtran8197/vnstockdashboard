from django.db import models

from prices.constants.price import TimeRangeType, TIME_RANGE_TYPE_CHOICES
from stocks.models import Stock


class FinancialRatio(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock_financial_ratio"
    )
    ticker = models.CharField(max_length=10)
    time_range_type = models.PositiveSmallIntegerField(
        choices=TIME_RANGE_TYPE_CHOICES, default=TimeRangeType.YEARLY
    )
    year = models.CharField(max_length=10, default="")
    quarter = models.CharField(max_length=10, default="")
    pe = models.FloatField()
    pb = models.FloatField()
    roe = models.FloatField()
    roa = models.FloatField()
    eps = models.FloatField()
    book_value_per_share = models.FloatField()
    interest_margin = models.FloatField()
    non_interest_on_toi = models.FloatField()
    bad_debt_percentage = models.FloatField()
    provision_on_bad_debt = models.FloatField()
    cost_of_financing = models.FloatField()
    equity_on_total_asset = models.FloatField()
    equity_on_loan = models.FloatField()
    cost_to_income = models.FloatField()
    equity_on_liability = models.FloatField()
    eps_change = models.FloatField()
    asset_on_equity = models.FloatField()
    pre_provision_on_toi = models.FloatField()
    post_tax_on_toi = models.FloatField()
    loan_on_earn_asset = models.FloatField()
    loan_on_asset = models.FloatField()
    loan_on_deposit = models.FloatField()
    deposit_on_earn_asset = models.FloatField()
    bad_debt_on_asset = models.FloatField()
    liquidity_on_liability = models.FloatField()
    payable_on_equity = models.FloatField()
    cancel_debt = models.FloatField()
    book_value_per_share_change = models.FloatField()
    credit_growth = models.FloatField()

    class Meta:
        db_table = "financial_ratios"


class IncomeStatement(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock_income_statement"
    )
    ticker = models.CharField(max_length=10)
    time_range_type = models.PositiveSmallIntegerField(
        choices=TIME_RANGE_TYPE_CHOICES, default=TimeRangeType.YEARLY
    )
    time_value = models.CharField(max_length=50)
    revenue = models.FloatField()
    year_revenue_growth = models.FloatField()
    quarter_revenue_growth = models.FloatField()
    cost_of_good_sold = models.FloatField()
    gross_profit = models.FloatField()
    operation_expense = models.FloatField()
    operation_profit = models.FloatField()
    year_operation_profit_growth = models.FloatField()
    quarter_operation_profit_growth = models.FloatField()
    interest_expense = models.FloatField()
    pre_tax_profit = models.FloatField()
    post_tax_profit = models.FloatField()
    share_holder_income = models.FloatField()
    year_share_holder_income_growth = models.FloatField()
    quarter_share_holder_income_growth = models.FloatField()
    invest_profit = models.FloatField()
    service_profit = models.FloatField()
    other_profit = models.FloatField()
    provision_expense = models.FloatField()
    operation_income = models.FloatField()
    ebitda = models.FloatField()

    class Meta:
        db_table = "income_statements"


class BalanceSheet(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock_balance_sheet"
    )
    ticker = models.CharField(max_length=10)
    time_range_type = models.PositiveSmallIntegerField(
        choices=TIME_RANGE_TYPE_CHOICES, default=TimeRangeType.YEARLY
    )
    year = models.CharField(max_length=10, default="")
    quarter = models.CharField(max_length=10, default="")
    short_asset = models.FloatField()
    cash = models.FloatField()
    short_invest = models.FloatField()
    short_receivable = models.FloatField()
    inventory = models.FloatField()
    long_asset = models.FloatField()
    fixed_asset = models.FloatField()
    asset = models.FloatField()
    debt = models.FloatField()
    short_debt = models.FloatField()
    long_debt = models.FloatField()
    equity = models.FloatField()
    capital = models.FloatField()
    central_bank_deposit = models.FloatField()
    other_bank_deposit = models.FloatField()
    other_bank_loan = models.FloatField()
    stock_invest = models.FloatField()
    customer_loan = models.FloatField()
    bad_load = models.FloatField()
    provision = models.FloatField()
    net_customer_loan = models.FloatField()
    other_asset = models.FloatField()
    other_bank_credit = models.FloatField()
    owe_other_bank = models.FloatField()
    owe_central_bank = models.FloatField()
    valuable_paper = models.FloatField()
    payable_interest = models.FloatField()
    receivable_interest = models.FloatField()
    deposit = models.FloatField()
    other_debt = models.FloatField()
    fund = models.FloatField()
    un_distributed_income = models.FloatField()
    minor_share_holder_profit = models.FloatField()
    payable = models.FloatField()

    class Meta:
        db_table = "balance_sheets"


class InsiderDeals(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="company_insider_deals"
    )
    ticker = models.CharField(max_length=20)
    deal_announce_date = models.CharField(max_length=11)
    deal_method = models.CharField(max_length=100)
    deal_action = models.CharField(max_length=3)
    deal_quantity = models.FloatField()
    deal_price = models.FloatField()
    deal_ratio = models.FloatField()

    class Meta:
        db_table = "company_insider_deals"


class FinancialFlow(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="financial_flow"
    )
    ticker = models.CharField(max_length=10)
    time_range_type = models.PositiveSmallIntegerField(
        choices=TIME_RANGE_TYPE_CHOICES, default=TimeRangeType.YEARLY
    )
    year = models.CharField(max_length=10, default="")
    quarter = models.CharField(max_length=10, default="")
    invest_code = models.FloatField()
    from_invest = models.FloatField()
    from_financial = models.FloatField()
    from_sale = models.FloatField()
    free_cash_flow = models.FloatField()

    class Meta:
        db_table = "financial_flows"
