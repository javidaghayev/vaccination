from django.urls import path
from vaccin import views

app_name = 'vaccin'

urlpatterns = [
    path('', views.VaccineList.as_view(), name='list'),
    path('<int:pk>/', views.VaccineDetail.as_view(), name='detail'),
    path('create/', views.VaccineCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateVaccine.as_view(), name='update'),
    path('delete/<int:pk>/', views.VaccineDelete.as_view(), name='delete'),
]
