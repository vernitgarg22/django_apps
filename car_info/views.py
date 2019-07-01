import requests
import datetime
from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from car_info.models import LicensePlateInfo

from cod_utils.util import date_json


@api_view(['POST'])
def add_polling_location(request):

    if not request.data.get('plate_num'):
        return Response({"message": "'plate_num' is required"}, status=status.HTTP_400_BAD_REQUEST)

    plate_num = request.data['plate_num']

    car_info_data = LicensePlateInfo.objects.filter(plate_num=plate_num)
    if car_info_data.exists():
        return Response({"message": "Error: plate number already added", "date_added": date_json(car_info_data[0].created_at)})

    car_info = LicensePlateInfo(plate_num=plate_num)
    car_info.save()

    return Response({"message": "Plate number added", "date_added": date_json(car_info.created_at)}, status=status.HTTP_201_CREATED)
