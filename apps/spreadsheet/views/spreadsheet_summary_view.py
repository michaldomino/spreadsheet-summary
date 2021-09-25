import os
from typing import TYPE_CHECKING

import numpy as np
import pandas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.spreadsheet.non_data_models import SpreadsheetSummaryRequestModel
from apps.spreadsheet.serializers import SpreadsheetSummaryRequestSerializer
from apps.spreadsheet.services import StorageService

if TYPE_CHECKING:
    from pandas import DataFrame
    from rest_framework.request import Request


class SpreadsheetSummaryView(APIView):

    def post(self, request: 'Request'):
        request_serializer = SpreadsheetSummaryRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            try:
                request_model = SpreadsheetSummaryRequestModel.from_validated_data(request_serializer.validated_data)
                storage_service = StorageService()
                file = storage_service.open(request_model.file_name)
                data_frame: 'DataFrame' = pandas.read_excel(file.read(),
                                                            skiprows=request_model.header_row)
                column_names = [column_name.strip() for column_name in request_model.columns]
                data_frame = data_frame.rename(columns=lambda column: column.strip())
                a = data_frame[['CURRENT USD', 'CURRENT CAD']][0:-1].sum()
                b = a['CURRENT USD']
                f = 0
            except FileNotFoundError as e:
                return Response(data={'detail': f'File "{os.path.basename(e.filename)}" not uploaded.'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
