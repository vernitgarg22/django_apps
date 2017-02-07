import json
import requests
import urllib.parse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic

from .forms import WasteItemSearchForm, WasteItemResultsForm
from .models import WasteItem


def get_keywords_json():
    keywords = set()
    for item in WasteItem.objects.all():
        keywords.update(item.description.split(', ') + item.keywords.split(', '))
    return json.dumps(list(keywords))


class IndexView(generic.ListView):
    template_name = 'waste_wizard/index.html'
    model = WasteItem
    context_object_name = 'waste_item_list'

    def get(self, request, *args, **kwargs):
        list = self.get_queryset()
        keywords = get_keywords_json()
        return render(request, 'waste_wizard/index.html', 
            { 'form': WasteItemSearchForm(), 'waste_item_list': list, 'keywords': keywords })

    def get_queryset(self):
        return WasteItem.objects.order_by('description')[:128]


class ResultsView(generic.ListView):
    template_name = 'waste_wizard/results.html'
    model = WasteItem
    context_object_name = 'waste_item_results'

    def get(self, request, *args, **kwargs):
        self.description = args[0]
        return self.handle_request(request)

    def post(self, request, *args, **kwargs):
        form = WasteItemSearchForm(request.POST)
        if False == form.is_valid():
            return HttpResponse("Please try your search again")

        self.description = form.cleaned_data['description']
        return self.handle_request(request)

    def handle_request(self, request):
        results = self.get_queryset()
        keywords = get_keywords_json()
        return render(request, 'waste_wizard/results.html', 
            { 'form': WasteItemResultsForm(), 'waste_item_results': results, 'keywords': keywords })

    def get_queryset(self):
        results, message = self.keyword_search(self.description)
        return results

    def keyword_search(self, description):
        results = WasteItem.objects.filter(description__contains=description)
        if False == results.exists():
            results = WasteItem.objects.filter(keywords__contains=description)
        if False == results.exists():
            return results, "No results found for " + description
        return results.order_by('description')[:128], ''
