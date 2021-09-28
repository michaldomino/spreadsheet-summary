import os

from django.core.files.storage import DefaultStorage
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.spreadsheet.services import StorageService
from apps.spreadsheet.tests.resources import TEST_SPREADSHEET_XLSX
from apps.spreadsheet.tests.scripts.test_helpers import open_as_in_memory_uploaded_file

test_settings = override_settings(
    MEDIA_ROOT='/tmp/django/spreadsheet_summary/test/'
)


@test_settings
class TestSpreadsheetSummaryView(APITestCase):
    _SPREADSHEET_PATH = TEST_SPREADSHEET_XLSX

    def setUp(self) -> None:
        self.spreadsheet_file_name = os.path.basename(self._SPREADSHEET_PATH)
        self.header_row = 2
        self.summary_url = reverse('summary')

        self._upload_spreadsheet()
        super().setUp()

    def tearDown(self) -> None:
        DefaultStorage().delete(self.spreadsheet_file_name)
        super().tearDown()

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

    def test_summary_should_calculate_correctly_when_start_row_provided(self):
        request_data = {
            'file_name': self.spreadsheet_file_name,
            'header_row': self.header_row,
            'start_row': 3,
            'columns': ['ONE LINE', 'MULTI LINE TEXT', 'PERCENT']
        }
        expected_data = {
            'file': self.spreadsheet_file_name,
            'summary': [
                {'column': 'ONE LINE', 'sum': 28.0, 'avg': 4.666666666666667},
                {'column': 'MULTI LINE TEXT', 'sum': 516.912, 'avg': 86.152},
                {'column': 'PERCENT', 'sum': 2197.6608643, 'avg': 366.27681071666666}
            ]
        }

        response = self.client.post(self.summary_url, request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_summary_should_calculate_correctly_when_end_rows_skipped_provided(self):
        request_data = {
            'file_name': self.spreadsheet_file_name,
            'header_row': self.header_row,
            'end_rows_skipped': 2,
            'columns': ['ONE LINE', 'MULTI LINE TEXT', 'PERCENT']
        }
        expected_data = {
            'file': self.spreadsheet_file_name,
            'summary': [
                {'column': 'ONE LINE', 'sum': 15.5, 'avg': 2.5833333333333335},
                {'column': 'MULTI LINE TEXT', 'sum': 150.0, 'avg': 25.0},
                {'column': 'PERCENT', 'sum': 1098.8254322, 'avg': 183.13757203333333}
            ]
        }

        response = self.client.post(self.summary_url, request_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def _upload_spreadsheet(self):
        storage_service = StorageService()
        in_memory_file = open_as_in_memory_uploaded_file(self._SPREADSHEET_PATH)
        storage_service.save(in_memory_file)
