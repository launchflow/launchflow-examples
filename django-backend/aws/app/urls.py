from app import views
from app.admin import admin
from django.urls import path

urlpatterns = [
    path("", views.index),
    path("admin/", admin.site.urls),
]
