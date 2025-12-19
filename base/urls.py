from django.urls import re_path

from . import views

app_name = "base"
urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^get_app_data/$", views.get_app_data, name="get_app_data"),
    re_path(r"^iframe_index/$", views.iframe_index, name="iframe_index")
]


