from django.contrib import admin

from stocks.models import Stock, StockCategory, StockDividendHistory
from django.db.models import Q


# Register your models here.
class CategoryListFilter(admin.SimpleListFilter):
    title = "Category"
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        # generate the list of choices
        categories = StockCategory.objects.filter(level__in=[1,2,3])
        categories_data = []
        for category in categories:
            icb_name = category.name
            if category.level == 2:
                icb_name = "-- " + icb_name
            elif category.level == 3:
                icb_name = "---- " + icb_name
            categories_data.append((category.icb_code, icb_name))
        return categories_data

    def queryset(self, request, queryset):
        # filter the queryset by the selected value
        value = self.value()
        if value is not None:
            ft = Q(Q(category_id__parent_id_level_1=self.value()) | Q(category_id__parent_id_level_2=self.value()) | Q(category_id__parent_id_level_3=self.value()))
            return queryset.filter(ft)
        return queryset


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ["code", "name"]
    list_filter = (CategoryListFilter,)


@admin.register(StockDividendHistory)
class StockDividendHistoryAdmin(admin.ModelAdmin):
    @admin.display(description='exercise date')
    def formatted_exercise_date(self, obj):
        return obj.exercise_date.strftime('%Y-%m-%d')
    list_display = ('code', 'cash_year', 'formatted_exercise_date', 'cash_dividend_percentage', 'issue_method')
    ordering = ('-cash_year', '-exercise_date')





