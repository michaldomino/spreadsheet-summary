import os

from django.core.files.storage import DefaultStorage
from django.test import override_settings, TestCase

from apps.spreadsheet.services import StorageService
from apps.spreadsheet.tests.resources import TEST_SPREADSHEET_XLSX
from apps.spreadsheet.tests.scripts.assert_not_raises_mixin import AssertNotRaisesMixin
from apps.spreadsheet.tests.scripts.test_helpers import attempt_to_open_spreadsheet_using_default_storage, \
    open_as_in_memory_uploaded_file

test_settings = override_settings(
    MEDIA_ROOT='/tmp/django/spreadsheet_summary/test/'
)


@test_settings
class TestStorageService(TestCase, AssertNotRaisesMixin):
    _SPREADSHEET_PATH = TEST_SPREADSHEET_XLSX

    def setUp(self) -> None:
        self.spreadsheet_file_name = os.path.basename(self._SPREADSHEET_PATH)
        self.storage_service = StorageService()
        self.default_storage = DefaultStorage()
        super().setUp()

    def tearDown(self) -> None:
        self.default_storage.delete(self.spreadsheet_file_name)
        super().tearDown()

    def test_service_should_save_when_correct(self):
        in_memory_file = open_as_in_memory_uploaded_file(self._SPREADSHEET_PATH)
        self.assertRaises(FileNotFoundError, attempt_to_open_spreadsheet_using_default_storage)

        self.storage_service.save(in_memory_file)

        self.assertNotRaises(attempt_to_open_spreadsheet_using_default_storage)

    def test_service_should_open_when_saved(self):
        in_memory_file = open_as_in_memory_uploaded_file(self._SPREADSHEET_PATH)
        self.default_storage.save(in_memory_file.name, in_memory_file.file)

        self.assertNotRaises(attempt_to_open_spreadsheet_using_default_storage)

    def test_service_should_raise_file_not_found_exception_when_file_does_not_exist(self):
        def open_not_existing_file(): self.storage_service.open('does_not_exist.xlsx')

        self.assertRaises(FileNotFoundError, open_not_existing_file)
