import json
import requests

from Lib import base64

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cod_utils.cod_logger import CODLogger

from photo_survey.models import Image, ImageMetadata


@api_view(['GET'])
def get_survey_count(request, parcel_id):
    """
    Get number of images that exist currently for the given parcel.
    TODO: Clarify if we can identify a single survey, and return number of surveys available?
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    image_metadata = ImageMetadata.objects.filter(parcel_id=parcel_id)
    content = { "count": len(image_metadata) }

    return Response(content)


@api_view(['GET'])
def get_metadata(request, parcel_id):
    """
    Get photos and survey data for the given parcel
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    images = []
    image_metadata = ImageMetadata.objects.filter(parcel_id=parcel_id)
    for img_meta in image_metadata:
        images.append(img_meta.image.file_path)

    return Response({ "images": images })


@api_view(['GET'])
def get_image(request, image_path):
    """
    Return the given photo
    """

    CODLogger.instance().log_api_call(name=__name__, msg=request.path)

    data = None
    # image_path = 'photo_survey/demo_image.jpg'
    # image_path = DJANGO_HOME + "/photo_survey/demo_images/demo_image1.jpg"
    full_path = settings.AUTO_LOADED_DATA["PHOTO_SURVEY_IMAGE_PATH"] + image_path
    with open(full_path, 'rb') as f:
        data = f.read()

    encoded = base64.b64encode(data)

    return Response(encoded)
