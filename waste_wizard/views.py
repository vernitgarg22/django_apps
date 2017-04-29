import json
import math
import requests
import urllib.parse

from itertools import zip_longest

from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.views import generic

from .forms import WasteItemSearchForm, WasteItemResultsForm
from .models import WasteItem


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

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
        keywords = get_keywords_json()
        return render(request, 'waste_wizard/index.html', 
            { 'form': WasteItemSearchForm(), 'keywords': keywords })


class ItemsView(generic.ListView):
    template_name = 'waste_wizard/items.html'
    model = WasteItem
    context_object_name = 'waste_item_list'

    def get(self, request, *args, **kwargs):

        context = { 'form': WasteItemSearchForm() }
        items = self.get_queryset()

        keywords = {}
        for item in items:
            letter = item.description.upper()[0]
            if not keywords.get(letter):
                keywords[letter] = []
            keywords[letter].append(item.description)

        arr = [ { 'letter': c, 'keywords': keywords.get(c) } for c in char_range('A', 'Z') if keywords.get(c) ]

        MIDDLE = int(len(arr) / 2)
        if len(arr) % 2 == 1:
            MIDDLE = MIDDLE + 1

        l1 = [ arr[idx] for idx in range(MIDDLE) ]
        l2 = [ arr[idx] for idx in range(MIDDLE, len(arr)) ]
        context['tuples'] = zip_longest(l1, l2)

        return render(request, 'waste_wizard/items.html', context)

    def get_queryset(self):
        return WasteItem.objects.order_by('description')[:128]


class ResultsView(generic.ListView):
    template_name = 'waste_wizard/results.html'
    model = WasteItem
    context_object_name = 'waste_item_results'

    def get(self, request, *args, **kwargs):
        self.description = args[0] if args else ''
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


class DetailView(generic.ListView):
    template_name = 'waste_wizard/detail.html'
    model = WasteItem
    context_object_name = 'waste_item'

    def get(self, request, *args, **kwargs):
        try:
            waste_item = WasteItem.objects.get(description=args[0])
        except WasteItem.DoesNotExist:
            return HttpResponseNotFound("<h2>Waste item '" + args[0] + "' does not exist</h2>")
        image_url = "waste_wizard/images/" + waste_item.image_url if waste_item.image_url else ""
        return render(request, 'waste_wizard/detail.html', 
            { 'form': WasteItemResultsForm(), 'waste_item': waste_item, 'image_url': image_url })
