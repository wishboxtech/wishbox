from django.urls import path

from src.api.views.storage.upload_file.view import UploadFile

storage_urlpatterns = [
    path("upload/", UploadFile.as_view(), name="upload_media"),
]
