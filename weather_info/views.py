import json
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

import xmltodict
from collections import OrderedDict


def remover(x):
    if isinstance(x,list): return [remover(y) for y in x]
    elif isinstance(x,OrderedDict):
        for ky in list(x.keys()):
            if ky[0] in ["@","#"]: 
                x[ky[1:]] = remover(x[ky])
                del x[ky]
            else: x[ky] = remover(x[ky])
        return x
    else: return x


@api_view(['GET'])
def get_latest(request, lat="42.331427", lon="-83.045754"):
    """
    Get latest weather data
    """

    if request.query_params.get('lat'):
        lat = request.query_params.get('lat')
    if request.query_params.get('lon'):
        lon = request.query_params.get('lon')

    url = "https://forecast.weather.gov/MapClick.php?lat={0}&lon={1}&unit=0&lg=english&FcstType=dwml".format(lat, lon)

    response = requests.get(url, timeout=60)
    data = xmltodict.parse(response.text)
    new_data = remover(data)

    return Response(new_data)
