from rest_framework import serializers


class UploadSpreadsheetSerializer(serializers.Serializer):
    file = serializers.FileField()
