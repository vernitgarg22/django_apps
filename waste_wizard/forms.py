from django import forms


class WasteItemSearchForm(forms.Form):
    description = forms.CharField(label='Describe the waste item', max_length=100)

class WasteItemResultsForm(forms.Form):
    description = forms.CharField(label='Describe another waste item', max_length=100)
