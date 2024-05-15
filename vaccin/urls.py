from django.urls import path
from vaccin import views

app_name = 'vaccin'

urlpatterns = [
    path('', views.VaccineList.as_view(), name='list'),
    path('<int:pk>/', views.VaccineDetail.as_view(), name='detail'),
    path('create/', views.VaccineCreate.as_view(), name='create'),
]
