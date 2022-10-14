from django import forms


class DatePickerInput(forms.DateInput):
    input_type = 'date'

# class MultipleChoiceInput(forms.TypedMultipleChoiceField):
#     input_type = 'select'