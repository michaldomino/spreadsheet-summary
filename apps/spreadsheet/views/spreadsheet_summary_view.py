import os
from typing import TYPE_CHECKING

import pandas
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.spreadsheet.non_data_models import SpreadsheetSummaryRequest, SpreadsheetSummaryResponse, Result
from apps.spreadsheet.serializers import SpreadsheetSummaryRequestSerializer, SpreadsheetSummaryResponseSerializer
from apps.spreadsheet.services import StorageService, SpreadsheetSummaryService

if TYPE_CHECKING:
    from pandas import DataFrame
    from rest_framework.request import Request


class SpreadsheetSummaryView(GenericAPIView):

    @swagger_auto_schema(request_body=SpreadsheetSummaryRequestSerializer(),
                         responses={200: SpreadsheetSummaryResponseSerializer()})
    def post(self, request: 'Request'):
        request_serializer = SpreadsheetSummaryRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            try:
                request_model = SpreadsheetSummaryRequest.from_validated_data(request_serializer.validated_data)
                data_frame = self._prepare_data_frame(request_model)
                column_names = [column_name.strip() for column_name in request_model.columns]
                spreadsheet_summary_service = SpreadsheetSummaryService(data_frame)
                sum_results = spreadsheet_summary_service.calculate_sum(column_names, request_model.start_row,
                                                                        request_model.end_rows_skipped)
                avg_results = spreadsheet_summary_service.calculate_average(column_names, request_model.start_row,
                                                                            request_model.end_rows_skipped)
                response = self._prepare_response(sum_results, avg_results, column_names, request_model.file_name)
                return response
            except FileNotFoundError as e:
                return Response(data={'detail': f'File "{os.path.basename(e.filename)}" not uploaded.'},
                                status=status.HTTP_400_BAD_REQUEST)
            except KeyError as e:
                return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _prepare_data_frame(request_model):
        storage_service = StorageService()
        file = storage_service.open(request_model.file_name)
        data_frame: 'DataFrame' = pandas.read_excel(file.read(), skiprows=request_model.header_row)
        return data_frame.rename(columns=lambda column: column.strip())

    @staticmethod
    def _prepare_response(sum_results, avg_results, column_names, file_name):
        results = [Result(column_name,
                          sum_results[column_name],
                          avg_results[column_name])
                   for column_name in column_names]
        response = SpreadsheetSummaryResponse(file_name, summary=results)
        response_serializer = SpreadsheetSummaryResponseSerializer(response)
        return Response(response_serializer.data)
