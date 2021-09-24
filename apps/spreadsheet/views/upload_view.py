from enum import Enum
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.spreadsheet.serializers.upload_serializer import UploadSerializer

if TYPE_CHECKING:
    from django.core.files.uploadedfile import InMemoryUploadedFile
    from rest_framework.request import Request


class UploadView(APIView):

    def post(self, request: 'Request'):
        try:
            # a: 'InMemoryUploadedFile' = request.data['file']
            serializer = UploadSerializer(data=request.data)
            if serializer.is_valid():
                b = serializer.validated_data['file']
                f = 0
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # serializer.data
        # a = serializer.is_valid()
        except KeyError as e:
            return Response(_ResponseDetails.FILE_FIELD_REQUIRED.value, status=status.HTTP_400_BAD_REQUEST)


class _ResponseDetails(Enum):
    FILE_FIELD_REQUIRED = {'file': ['This field is required.']}
