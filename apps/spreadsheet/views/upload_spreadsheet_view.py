from enum import Enum
from typing import TYPE_CHECKING

import pandas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.spreadsheet.serializers import UploadSpreadsheetSerializer

if TYPE_CHECKING:
    from pandas import DataFrame
    from django.core.files.uploadedfile import InMemoryUploadedFile
    from rest_framework.request import Request


class UploadSpreadsheetView(APIView):

    def post(self, request: 'Request'):
        try:
            # a: 'InMemoryUploadedFile' = request.data['file']
            serializer = UploadSpreadsheetSerializer(data=request.data)
            if serializer.is_valid():
                file: 'InMemoryUploadedFile' = serializer.validated_data['file']
                data_frame: 'DataFrame' = pandas.read_excel(file.read(), skiprows=2)
                # default_storage.save()
                # a = ''
                # a.endswith()
                # if not file.name.endswith(('xls', 'xlsx')):
                #     return
                # new_header = data_frame.il
                # new_header = data_frame.iloc[0]
                # data_frame = data_frame[2:]
                # data_frame.columns = new_header
                data_frame.sum()
                f = 0
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # serializer.data
        # a = serializer.is_valid()
        except KeyError as e:
            return Response(_ResponseDetails.FILE_FIELD_REQUIRED.value, status=status.HTTP_400_BAD_REQUEST)


class _ResponseDetails(Enum):
    FILE_FIELD_REQUIRED = {'file': ['This field is required.']}
