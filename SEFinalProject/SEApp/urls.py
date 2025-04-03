from django.urls import path
from . import views
# Define a List of url patterns
urlpatterns = [
    path('<int:id>', views.index, name = "index"),
    path("", views.home, name ="home")
]
