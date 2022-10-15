from django import forms
from .models import Expense, Category
from .widgets import DatePickerInput


class ExpenseSearchForm(forms.ModelForm):
    from_date = forms.DateField(widget=DatePickerInput, required=False)
    to_date = forms.DateField(widget=DatePickerInput, required=False)
    categories = forms.MultipleChoiceField(
        choices=((category.id, category.name) for category in Category.objects.all()),
        required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    # def __init__(self, *args, **kwargs):
    #     super(ExpenseSearchForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].required = False
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'
