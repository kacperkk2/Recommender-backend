from .views import ResultsView
from django.urls import path


urlpatterns = [
    path('', ResultsView.as_view())
]