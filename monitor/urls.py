from django.contrib import admin
from django.urls import path, include
from monitor import views as mviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', mviews.health),
    path('api/urls/', mviews.urls_list),
    path('api/results/', mviews.results_list),
    path('', include('django_prometheus.urls')),
]
