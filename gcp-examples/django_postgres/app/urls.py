from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_users),
    path("create/", views.create_user),
    path("<int:user_id>/", views.user_detail),
]
