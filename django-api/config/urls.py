from django.urls import include, path, re_path

from tracker.errors import unknown_route

urlpatterns = [
    path("api/", include("tracker.urls")),
    re_path(r"^.*$", unknown_route),    # cualquier otra ruta -> 404 en JSON
]