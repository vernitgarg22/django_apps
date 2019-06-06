# from django.contrib.syndication.views import Feed
# from django.urls import reverse

import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer


from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer

import xml.etree.ElementTree as ET



import pdb


@api_view(['GET'])
# @renderer_classes((XMLRenderer,))
def get_rss(request, format=None):


    # pdb.set_trace()


    url = "https://jobs.mitalent.org/rss/MiTalentJobs.aspx?ZIPCODE=48214"
    resp = requests.get(url)

    data = "<channel><item><title>sample title</title><guid>foobar</guid></item></channel>"
    return Response(data=data, content_type="application/rss+xml")
    data = resp.content

    pos = data.find(b"<rss")
    if pos:
        data = data[pos : ]

    response = Response(data=data)

    return response



    # root = ET.fromstring(resp.text)

    # data = {
    #     "channel": [
    #         {
    #             "item": {
    #                 "title": "Simulation Engineer"
    #             }
    #         }
    #     ]
    # }


    # # pdb.set_trace()


    # for channel in root.iter('channel'):

    #     # print('channel')

    #     for item in channel:

    #         # print('item')

    #         new_item = {}

    #         data["channel"].append(new_item)

    #         for val in item:

    #             print(val)

    #             # pdb.set_trace()
    
    # return Response(data=data, content_type="application/json")
