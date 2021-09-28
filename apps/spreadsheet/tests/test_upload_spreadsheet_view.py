import os

from django.core.files.storage import DefaultStorage
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.spreadsheet.services import StorageService
from apps.spreadsheet.tests.resources import TEST_SPREADSHEET_XLSX, TEXT_FILE_TXT

test_settings = override_settings(
    MEDIA_ROOT='/tmp/django/spreadsheet_summary/test/'
)


@test_settings
class TestUploadSpreadsheetView(APITestCase):
    _SPREADSHEET_PATH = TEST_SPREADSHEET_XLSX
    _TEXT_FILE_PATH = TEXT_FILE_TXT

    def setUp(self) -> None:
        self.spreadsheet_file_name = os.path.basename(self._SPREADSHEET_PATH)
        self.upload_url = reverse('upload')
        self.storage_service = StorageService()
        super().setUp()

    def tearDown(self) -> None:
        DefaultStorage().delete(self.spreadsheet_file_name)
        super().tearDown()

    def test_upload_should_return_ok_when_correct(self):
        with open(self._SPREADSHEET_PATH, 'rb') as file:
            request_data = {
                'file': file
            }

            response = self.client.post(self.upload_url, data=request_data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_should_return_ok_when_file_already_exist(self):
        with open(self._SPREADSHEET_PATH, 'rb') as file:
            request_data = {
                'file': file
            }
            self.client.post(self.upload_url, data=request_data)
            self.assertNotRaises(self.open_file)
        with open(self._SPREADSHEET_PATH, 'rb') as file:
            request_data = {
                'file': file
            }

            response = self.client.post(self.upload_url, data=request_data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_should_file_exist_when_uploaded(self):
        with open(self._SPREADSHEET_PATH, 'rb') as file:
            request_data = {
                'file': file
            }

            self.assertRaises(FileNotFoundError, self.open_file)
            self.client.post(self.upload_url, data=request_data)

            self.assertNotRaises(self.open_file)

    def test_upload_should_return_bad_request_when_incorrect_file_type(self):
        with open(self._TEXT_FILE_PATH, 'rb') as file:
            request_data = {
                'file': file
            }
            expected_data = {
                'detail': 'File is not an Excel spreadsheet'
            }

            response = self.client.post(self.upload_url, data=request_data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data, expected_data)

    def open_file(self):
        file = self.storage_service.open(self.spreadsheet_file_name)
        file.close()

    def assertNotRaises(self, callable):
        try:
            callable()
        except Exception as e:
            self.assertTrue(False, msg=f'Exception of type: "{type(e).__name__}" was thrown')
        self.assertTrue(True)
