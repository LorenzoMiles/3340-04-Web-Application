from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Define a List of url patterns
urlpatterns = [
    # Make the root URL redirect to login
    path('', views.redirect_to_login, name="root"),
    
    path('<int:id>', views.index, name="index"),
    path("home/", views.home, name="home"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='SEApp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]