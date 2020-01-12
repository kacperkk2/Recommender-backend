from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('algorithms/', include('algorithms.api.urls')),
    path('data_sets/', include('data_sets.api.urls')),
    path('results/', include('results.api.urls')),
    path('histories/', include('histories.api.urls'))
]
