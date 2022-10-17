from collections import OrderedDict
import datetime
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def total_amount(queryset):
    return sum([total for total in summary_per_category(queryset).values()])


def summary_per_year_month(queryset):
    summary = {}
    for expense in queryset:
        if f"{expense.date.year}-{expense.date.month}" not in summary:
            summary[f"{expense.date.year}-{expense.date.month}"] = expense.amount
        else:
            summary[f"{expense.date.year}-{expense.date.month}"] += expense.amount
    return summary
