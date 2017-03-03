from django import forms


class WasteItemSearchForm(forms.Form):
    description = forms.CharField(label='Search for a waste item', max_length=100)

class WasteItemResultsForm(forms.Form):
    description = forms.CharField(label='Search for another waste item', max_length=100)
