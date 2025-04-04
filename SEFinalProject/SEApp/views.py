from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
# Create your views here.
def index(response, id):
    return render(response, "SEApp/base.html", {})

def home(response):
    return render(response, "SEApp/home.html", {})

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    form = TaskForm()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    
    context = {'tasks': tasks, 'form': form}
    return render(request, 'SEApp/base.html', context)
