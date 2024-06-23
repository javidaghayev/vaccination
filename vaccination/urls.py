from django.urls import path
from vaccination import views

app_name = 'vaccination'

urlpatterns = [
    path('', views.VaccinationList.as_view(), name='vaccination-list'),
    path('detail/<int:pk>/', views.VaccinationDetail.as_view(), name='vaccination-detail'),
    path('choose-vaccine/', views.ChooseVaccine.as_view(), name='choose-vaccine'),
    path('choose-campaign/<int:vaccine_id>/', views.ChooseCampaign.as_view(), name='choose-campaign'),
    path('choose-slot/<int:campaign_id>/', views.ChooseSlot.as_view(), name='choose-slot'),
    path('confirm-vaccination/<int:campaign_id>/<int:slot_id>/', views.ConfirmVaccination.as_view(), name='confirm-vaccination'),
]