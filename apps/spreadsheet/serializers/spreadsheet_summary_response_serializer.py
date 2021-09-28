from rest_framework import serializers


class ResultSerializer(serializers.Serializer):
    column = serializers.CharField()
    sum = serializers.FloatField()
    avg = serializers.FloatField()


class SpreadsheetSummaryResponseSerializer(serializers.Serializer):
    file = serializers.CharField()
    summary = ResultSerializer(many=True)
