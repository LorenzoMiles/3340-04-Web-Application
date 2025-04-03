from django.urls import path
from . import views
# Define a List of url patterns
urlpatterns = [
    path('', views.index)
]