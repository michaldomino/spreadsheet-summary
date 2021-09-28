import io
import mimetypes
import os

from django.core.files.storage import DefaultStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.spreadsheet.tests.resources import TEST_SPREADSHEET_XLSX


def _get_file_size(file):
    file.seek(0)
    file.read()
    size = file.tell()
    file.seek(0)
    return size


def open_as_in_memory_uploaded_file(file_path):
    with open(file_path, 'rb') as file:
        file_object = io.BytesIO(file.read())
        name = os.path.basename(file.name)
        size = _get_file_size(file)
        content_type, charset = mimetypes.guess_type(name)
        return InMemoryUploadedFile(file_object, None, name, content_type, size, charset)


def attempt_to_open_spreadsheet_using_default_storage():
    file = DefaultStorage().open(os.path.basename(TEST_SPREADSHEET_XLSX))
    file.close()
