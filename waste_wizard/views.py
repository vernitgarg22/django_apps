import requests
import urllib.parse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic

from .forms import WasteItemSearchForm
from .models import WasteItem


class IndexView(generic.ListView):
    template_name = 'waste_wizard/index.html'
    model = WasteItem
    context_object_name = 'waste_item_list'

    def get(self, request, *args, **kwargs):
        form = WasteItemSearchForm()
        list = self.get_queryset()
        return render(request, 'waste_wizard/index.html', {'form': form, 'waste_item_list': list})

    def get_queryset(self):
        return WasteItem.objects.order_by('-description')[:128]

def results(request, description=None):
    if request.method == 'POST':
        form = WasteItemSearchForm(request.POST)
        if False == form.is_valid():
            return HttpResponse("Please try your search again")

        description = form.cleaned_data['description']

    waste_item_info = "No waste items match " + description
    results = WasteItem.objects.filter(description__contains=description)
    if False == results.exists():
        results = WasteItem.objects.filter(keywords__contains=description)
    if False == results.exists():
        return HttpResponse("No results found for " + description)

    waste_item = results[0]
    info = waste_item.description + ' - ' + waste_item.destination

    if waste_item.notes:
        info += '<br/>(Note: ' + waste_item.notes + ')'
    return HttpResponse(info)
