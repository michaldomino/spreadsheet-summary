from django.urls import path

from apps.spreadsheet.views.upload_view import UploadView

urlpatterns = [
    path('api/v1/upload', UploadView.as_view()),
]
