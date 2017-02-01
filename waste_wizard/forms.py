from django import forms


class WasteItemSearchForm(forms.Form):
    description = forms.CharField(label='Describe the waste item', max_length=100)
