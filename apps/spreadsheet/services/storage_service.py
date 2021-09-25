from django.core.files.storage import DefaultStorage


class StorageService:

    def __init__(self):
        self._storage = DefaultStorage()

    def save(self, file):
        file_name = file.name
        if self._storage.exists(file_name):
            self._storage.delete(file_name)
        self._storage.save(file_name, file)

    def open(self, file_name):
        return self._storage.open(file_name)
