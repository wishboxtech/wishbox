from django.urls import path

from src.api.views.storage import UploadFile

storage_urlpatterns = [
    path("upload/", UploadFile.as_view(), name="upload_media"),
]
