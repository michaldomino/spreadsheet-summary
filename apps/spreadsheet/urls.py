from django.urls import path

from apps.spreadsheet.views import UploadSpreadsheetView

urlpatterns = [
    path('api/v1/upload', UploadSpreadsheetView.as_view()),
]
