import zipfile
from typing import TYPE_CHECKING

import openpyxl
from drf_yasg import renderers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, parsers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.spreadsheet.serializers import UploadSpreadsheetSerializer
from apps.spreadsheet.services import StorageService

if TYPE_CHECKING:
    from rest_framework.request import Request


class UploadSpreadsheetView(GenericAPIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = UploadSpreadsheetSerializer

    @swagger_auto_schema(responses={200: ''})
    def post(self, request: 'Request'):
        serializer = UploadSpreadsheetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                storage_service = StorageService()
                file = serializer.validated_data['file']
                self._check_file(file)
                storage_service.save(file)
                return Response(status=status.HTTP_200_OK)
            except zipfile.BadZipfile as e:
                return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _check_file(file):
        try:
            file = openpyxl.open(file)
        except zipfile.BadZipfile:
            raise zipfile.BadZipfile('File is not an Excel spreadsheet')
        file.close()
