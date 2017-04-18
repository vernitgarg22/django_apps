import requests

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def list_services(request):

    lat="42.331427"
    lon="-83.045754"

    url = "https://seeclickfix.com/open311/v2/services.json?lat={0}&long={1}".format(lat, lon)

    response = requests.get(url)
    return Response(response.json())


@api_view(['POST'])
def report(request):
    """
    Post a suspected illegal dumping
    """

    SERVER = "test.seeclickfix.com"

    # TODO REVIEW uncomment this once we are ready for prime time
    # if not settings.DEBUG:
    #     SERVER = "seeclickfix.com"

    API_KEY="24624f71bee008cfbf70a92b3e4ff18d2ebaa614"

    lat="42.331427"
    lon="-83.045754"

    SERVICE_CODE = "8645"
    SERVICE_NAME = "Illegal Dumping / Illegal Dump Sites"

    # url = "https://{0}/dev/v2/requests.xml?service_code={1}&lat={2}&long={3}".format(SERVER, SERVICE_CODE, lat, lon)
    # url = url + "&description=sofa%20illegally%20dumped"

    url = "https://{0}/dev/v2/requests.json".format(SERVER)
    params = "api_key={0}&service_code={1}&lat={2}&long={3}&description=sofa".format(API_KEY, SERVICE_CODE, lat, lon)

    response = requests.post(url, data=params)

    if response.status_code not in [200, 201]:
        return Response({ "error": True, "status_code": response.status_code })

    content = response.content

    return Response(response.json())
