from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
#    path('news/', views.news_home, name='news_name'),
    path('about', views.about, name='about'),
    path('table/', views.csv_table, name='table'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
