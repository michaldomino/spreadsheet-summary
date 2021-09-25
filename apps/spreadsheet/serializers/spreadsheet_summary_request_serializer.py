from rest_framework import serializers


class SpreadsheetSummaryRequestSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    start_row = serializers.IntegerField()
    columns = serializers.ListField(child=serializers.CharField())
