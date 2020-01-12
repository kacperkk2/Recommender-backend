from django.urls import path

from .views import AlgorithmListView


urlpatterns = [
    path('', AlgorithmListView.as_view())
]