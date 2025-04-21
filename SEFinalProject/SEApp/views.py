from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Task, UserProfile
from .forms import TaskForm, UserRegisterForm, TaskStatusForm


def index(response, id):
    return render(response, "SEApp/base.html", {})

def home(request):
    tasks = Task.objects.all()
    return render(request, "SEApp/home.html", {'tasks': tasks})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            UserProfile.objects.create(user=user, user_type=user_type)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'SEApp/register.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'SEApp/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Try to get user profile, create one if it doesn't exist
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a default profile (you can choose the default type)
        user_profile = UserProfile.objects.create(user=request.user, user_type='assignee')
    # Check if user is assignee (can only update status)
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == 'assignee' and request.user in task.assigned_to.all():
        if request.method == 'POST':
            form = TaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task status updated successfully!')
                return redirect('task_detail', task_id=task.id)
        else:
            form = TaskStatusForm(instance=task)
        return render(request, 'SEApp/task_detail.html', {'task': task, 'form': form})
    
    # For task assigners (full edit capabilities)
    elif user_profile.user_type == 'assigner':
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task updated successfully!')
                return redirect('task_detail', task_id=task.id)
        else:
            form = TaskForm(instance=task)
        return render(request, 'SEApp/task_detail.html', {'task': task, 'form': form})
    
    # For users who are neither assigners nor assignees of this task
    return render(request, 'SEApp/task_detail.html', {'task': task})

@login_required
def create_task(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type != 'assigner':
        messages.error(request, 'You do not have permission to create tasks.')
        return redirect('task_list')
        
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Save the many-to-many relationships
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'SEApp/create_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.user_type != 'assigner':
        messages.error(request, 'You do not have permission to delete tasks.')
        return redirect('task_list')
        
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'SEApp/delete_task.html', {'task': task})

# Add this new function

def redirect_to_login(request):
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    # Otherwise redirect to login
    return redirect('login')

# Add this function to your views.py
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')