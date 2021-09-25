from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.spreadsheet.serializers import UploadSpreadsheetSerializer
from apps.spreadsheet.services import StorageService

if TYPE_CHECKING:
    from rest_framework.request import Request


class UploadSpreadsheetView(APIView):

    def post(self, request: 'Request'):
        serializer = UploadSpreadsheetSerializer(data=request.data)
        if serializer.is_valid():
            storage_service = StorageService()
            file = serializer.validated_data['file']
            storage_service.save(file)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
