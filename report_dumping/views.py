import os
import requests

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.contrib.django_orm import Storage

# from .models import CredentialsModel


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.environ['DJANGO_HOME'] + '/client_secrets.json'

# TODO get this working
# FLOW = flow_from_clientsecrets(
#     CLIENT_SECRETS,
#     scope = 'https://seeclickfix.com/detroit',
#     redirect_uri = 'https://apis.detroitmi.gov/reportdumping')


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

    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("plus", "v1", http=http)
        activities = service.activities()
        activitylist = activities.list(collection='public',
                                       userId='me').execute()
        logging.info(activitylist)

        return render(request, 'plus/welcome.html', { 'activitylist': activitylist, })






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
