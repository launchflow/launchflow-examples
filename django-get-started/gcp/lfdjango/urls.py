from django.urls import path
from app import views

urlpatterns = [
    path('', views.get_name, name='get_name'),
    path('post_name/', views.post_name, name='post_name'),
]
