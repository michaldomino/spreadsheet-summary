from rest_framework import serializers


class SpreadsheetSummaryRequestSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    header_row = serializers.IntegerField(default=0)
    start_row = serializers.IntegerField(default=0)
    end_rows_skipped = serializers.IntegerField(default=0)
    columns = serializers.ListField(child=serializers.CharField())
