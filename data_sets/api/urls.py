from django.urls import path

from .views import DataSetListView


urlpatterns = [
    path('', DataSetListView.as_view())
]