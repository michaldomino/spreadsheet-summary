import os
from typing import TYPE_CHECKING

import numpy as np
import pandas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
                storage_service = StorageService()
                file = storage_service.open(request_serializer.validated_data['file_name'])
                data_frame: 'DataFrame' = pandas.read_excel(file.read(),
                                                            skiprows=request_serializer.validated_data['start_row'])
                column_names = [column_name.strip() for column_name in request_serializer.validated_data['columns']]
                data_frame = data_frame.rename(columns=lambda column: column.strip())
                x = data_frame[column_names[0]].sum()
                a = data_frame[column_names[0]][0:-1].sum()
                y = np.sum(data_frame.groupby(by=column_names[0]).sum())
                z = data_frame.groupby(column_names[0]).sum().sum()

                x1 = data_frame[column_names[0]].mean(skipna=True)
                y1 = np.mean(data_frame.groupby(by=column_names[0]).mean())
                z1 = data_frame.groupby(column_names[0]).mean().mean()
                f = 0
            except FileNotFoundError as e:
                return Response(data={'detail': f'File "{os.path.basename(e.filename)}" not uploaded.'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
