from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from BirthdayApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("favicon.ico", views.favicon),
    path("admin/", admin.site.urls),
    path("api/", include("BirthdayApp.urls")),
    # Serves uploaded photos (fine for a small personal site)
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]