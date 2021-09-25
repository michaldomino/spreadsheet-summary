from django.core.files.storage import DefaultStorage


class StorageService:

    def __init__(self):
        self._storage = DefaultStorage()

    def save(self, file):
        self._storage.save(file.name, file)

    def open(self, file_name):
        return self._storage.open(file_name)
