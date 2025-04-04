from django.urls import path
from . import views

# Define a List of url patterns
urlpatterns = [
    path('<int:id>', views.index, name="index"),
    path("home/", views.home, name="home"),  
    path('', views.task_list, name='task_list'),
]
