from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("verify/", views.verify, name="verify"),
    path("setting/", views.setting, name="setting"),
    path("split/", views.split, name="split"),
    path("upload_audio/", views.upload_audio, name="upload_audio"),
]