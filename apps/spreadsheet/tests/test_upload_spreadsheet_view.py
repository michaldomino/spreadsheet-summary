import os

from django.core.files.storage import DefaultStorage
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

test_settings = override_settings(
    MEDIA_ROOT='/tmp/django/spreadsheet_summary/test/'
)


@test_settings
class TestUploadSpreadsheetView(APITestCase):
    _SPREADSHEET_PATH = 'apps/spreadsheet/tests/resources/test_spreadsheet.xlsx'

    def setUp(self) -> None:
        self.spreadsheet_file_name = os.path.basename(self._SPREADSHEET_PATH)
        self.upload_url = reverse('upload')
        super().setUp()

    def tearDown(self) -> None:
        DefaultStorage().delete(self.spreadsheet_file_name)
        super().tearDown()

    def test_upload_should_return_ok_when_correct(self):
        with open(self._SPREADSHEET_PATH, 'rb') as file:
            form = {
                'file': file
            }

            response = self.client.post(self.upload_url, data=form)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
