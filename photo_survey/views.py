import json
import os
import requests

from Lib import base64

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cod_utils.cod_logger import CODLogger


@api_view(['GET'])
def get_survey_count(request, parcel_id):
    """
    Get number of surveys that exist currently for the given parcel
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    content = { "count": 1 }

    return Response(content)


@api_view(['GET'])
def get_photos(request, parcel_id):
    """
    Get photos and survey data for the given parcel
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    content = { "images": [ "demo_image_id" ] }

    return Response(content)


@api_view(['GET'])
def get_image(request, image_id):
    """
    Return the given photo
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    DJANGO_HOME = os.environ['DJANGO_HOME']

    data = None
    # image_path = 'photo_survey/demo_image.jpg'
    image_path = DJANGO_HOME + "/photo_survey/demo_images/demo_image1.jpg"
    with open(image_path, 'rb') as f:
        data = f.read()
    
    encoded = base64.b64encode(data)

    return Response(encoded)
