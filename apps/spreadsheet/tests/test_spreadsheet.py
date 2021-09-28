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
        self.spreadsheet_file_name = os.path.basename(self._SPREADSHEET_PATH)
        self.header_row = 2
        self.summary_url = reverse('summary')

        self._upload_spreadsheet()
        return super().setUp()

    def tearDown(self) -> None:
        DefaultStorage().delete(self.spreadsheet_file_name)
        return super().tearDown()

    def test_summary_should_return_ok_when_correct(self):
        data = {
            'file_name': self.spreadsheet_file_name,
            'header_row': self.header_row,
            'columns': ['ONE LINE']
        }

        response = self.client.post(self.summary_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_summary_should_calculate_correctly_when_correct(self):
        request_data = {
            'file_name': self.spreadsheet_file_name,
            'header_row': self.header_row,
            'columns': ['ONE LINE', 'MULTI LINE TEXT', 'PERCENT']
        }
        expected_data = {
            'file': self.spreadsheet_file_name,
            'summary': [
                {'column': 'ONE LINE', 'sum': 31.0, 'avg': 3.875},
                {'column': 'MULTI LINE TEXT', 'sum': 546.912, 'avg': 68.364},
                {'column': 'PERCENT', 'sum': 2197.6708644, 'avg': 274.70885805}
            ]
        }

        response = self.client.post(self.summary_url, request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_summary_should_return_bad_request_when_file_does_not_exist(self):
        request_data = {
            'file_name': 'does_not_exist.xlsx',
            'columns': ['ONE LINE']
        }
        expected_data = {
            'detail': 'File "does_not_exist.xlsx" not uploaded.'
        }

        response = self.client.post(self.summary_url, request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_summary_should_return_bad_request_when_column_does_not_exist(self):
        request_data = {
            'file_name': self.spreadsheet_file_name,
            'header_row': self.header_row,
            'columns': ['NOT EXISTING COLUMN']
        }
        expected_data = {
            'details': ['Columns: [\'NOT EXISTING COLUMN\'] do not exist.']
        }

        response = self.client.post(self.summary_url, request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_summary_should_return_bad_request_when_file_name_not_provided(self):
        request_data = {
            'file_name': self.spreadsheet_file_name,
        }
        expected_data = {
            'columns': ['This field is required.']
        }

        response = self.client.post(self.summary_url, request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_summary_should_return_bad_request_when_columns_not_provided(self):
        request_data = {
            'columns': ['ONE LINE']
        }
        expected_data = {
            'file_name': ['This field is required.']
        }

        response = self.client.post(self.summary_url, request_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

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
