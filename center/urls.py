from django.urls import path
from center import views


urlpatterns = [
    path('', views.center_list, name='list')
]