from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.spreadsheet.serializers import SpreadsheetSummaryRequestSerializer
from apps.spreadsheet.services import StorageService

if TYPE_CHECKING:
    from rest_framework.request import Request


class SpreadsheetSummaryView(APIView):

    def post(self, request: 'Request'):
        request_serializer = SpreadsheetSummaryRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            storage_service = StorageService()
            file = storage_service.open(request_serializer.validated_data['file_name'])
            f = 0
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
