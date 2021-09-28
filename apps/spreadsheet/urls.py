from django.urls import path

from apps.spreadsheet.views import UploadSpreadsheetView, SpreadsheetSummaryView

urlpatterns = [
    path('api/v1/summary', SpreadsheetSummaryView.as_view(), name='summary'),
    path('api/v1/upload', UploadSpreadsheetView.as_view(), name='upload'),
]
