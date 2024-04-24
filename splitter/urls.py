from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("verify/", views.verify, name="verify"),
    path("setting/", views.setting, name="setting"),
    path("upload_audio/", views.upload_audio, name="upload_audio"),
    path("output_exist/", views.output_exist, name="output_exist"),
    path("split/", views.split, name="split"),
    path("download/<str:file_name>/", views.download, name="download"),
    # path("download_file/", views.FileDownloadView.as_view(), name="download_file"),
    path("download_file/", views.download_file, name="download_file"),
]