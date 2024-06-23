from django.urls import path
from campaign import views


app_name = 'campaign'
urlpatterns = [
    path('', views.CampaignViewList.as_view(), name='campaign-list'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('create/', views.CampaignCreateView.as_view(), name='campaign-create'),
    path('create/<int:pk>/', views.CampaignUpdateView.as_view(), name='campaign-update'),
    path('delete/<int:pk>/', views.CampaignDeleteView.as_view(), name='campaign-delete'),

    #SLOT
    path('<int:campaign_id>/slot/', views.SlotListView.as_view(), name='slot-list'),
    path('slot/<int:pk>', views.SlotDetailView.as_view(), name='slot-detail'),
    path('<int:campaign_id>/slot/create/', views.SlotCreateView.as_view(), name='slot-create'),
    path('slot/update/<int:pk>', views.SlotUpdateView.as_view(), name='slot-update'),
    path('slot/delete/<int:pk>', views.SlotDeleteView.as_view(), name='slot-delete'),
]