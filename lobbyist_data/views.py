import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    return HttpResponse("Hello, world. You're at the lookup index.")

@api_view(['GET'])
def lookup(request, format=None):
    """
    List lobbyist data
    """
    if request.method == 'GET':
        content = { "foo": "bar" }
        return Response(content)