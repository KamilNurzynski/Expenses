from django.core.paginator import Paginator
from django.views.generic.list import ListView
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, total_amount, summary_per_year_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')
            categories = form.cleaned_data.get('categories')
            if name:
                queryset = queryset.filter(name__icontains=name).order_by('date')
            if categories:
                queryset = queryset.filter(category__pk__in=categories).order_by('category')
            if from_date:
                queryset = queryset.filter(date__gte=from_date)
            if to_date:
                queryset = queryset.filter(date__lte=to_date)
            if from_date and to_date:
                queryset = queryset.filter(date__range=(from_date, to_date)).order_by('date')
            if name and from_date and to_date:
                queryset = queryset.filter(name__icontains=name, date__range=(from_date, to_date)).order_by('date')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount=total_amount(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        expenses = Expense.objects.all()
        expenses_of_category = {category.name: 0 for category in queryset}
        for expense in expenses:
            expenses_of_category[expense.category.name] += 1

        return super().get_context_data(
            object_list=queryset,
            expenses_of_category=expenses_of_category,
            **kwargs)
