from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('center/', include(('center.urls'), namespace='center')),
    path('vaccine/', include(('vaccin.urls'), namespace='vaccin')),
    path('accounts/', include(('user.urls'), namespace='user')),
    path('campaign/', include(('campaign.urls'), namespace='campaign')),
    path('vaccination/', include(('vaccination.urls'), namespace='vaccination')),
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


admin.site.site_header = 'Book My Vaccine'
admin.site.site_title = 'Book My Vaccine'
admin.site.index_title = 'Admin Panel'

