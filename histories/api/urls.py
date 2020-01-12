from .views import HistoriesView
from django.urls import path


urlpatterns = [
    path('', HistoriesView.as_view())
]