import io
import os

from django.core.files.storage import DefaultStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import override_settings
from django.urls import reverse
from openpyxl.packaging.manifest import mimetypes
from rest_framework import status
from rest_framework.test import APITestCase

from apps.spreadsheet.services import StorageService

test_settings = override_settings(
    MEDIA_ROOT='/tmp/django/spreadsheet_summary/test/'
)


@test_settings
class TestSpreadsheetView(APITestCase):
    _SPREADSHEET_PATH = 'apps/spreadsheet/tests/resources/test_spreadsheet.xlsx'

    def setUp(self) -> None:
        self._upload_spreadsheet()
        return super().setUp()

    def tearDown(self) -> None:
        file_name = os.path.basename(self._SPREADSHEET_PATH)
        DefaultStorage().delete(file_name)
        return super().tearDown()

    def test_summary_should_return_ok_when_correct(self):
        data = {
            'file_name': 'test_spreadsheet.xlsx',
            'header_row': 2,
            'columns': ['ONE LINE']
        }

        response = self.client.post(reverse('summary'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @staticmethod
    def _get_file_size(file):
        file.seek(0)
        file.read()
        size = file.tell()
        file.seek(0)
        return size

    def _upload_spreadsheet(self):
        storage_service = StorageService()
        with open(self._SPREADSHEET_PATH, 'rb') as file:
            file_object = io.BytesIO(file.read())
            name = os.path.basename(file.name)
            size = self._get_file_size(file)
            content_type, charset = mimetypes.guess_type(name)
            in_memory_file = InMemoryUploadedFile(file_object, None, name, content_type, size, charset)
            storage_service.save(in_memory_file)
