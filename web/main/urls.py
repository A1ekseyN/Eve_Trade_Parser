from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
#    path('news/', views.news_home, name='news_name'),
    path('about', views.about, name='about'),
    path('state_protectorate', views.json_table, name='state_protectorate'),
    path('lpstore/', views.lpstore, name='lpstore')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
