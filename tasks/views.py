from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils import timezone
from .forms import TaskForm
from .models import Task
# Create your views here.

def home(request):
    return render(request, 'home.html')

def tasks(request):
   tasks = Task.objects.filter(user=request.user)
   
   return render(request, 'tasks.html',{
       'tasks':tasks
   })
 
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    if request.method == 'POST':
        try: 
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'please provide valida data'
        })
          
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, task_id, user = request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', { 'task':task, 'form':form})
    
    if request.method== 'POST':
        try:
            task = get_object_or_404(Task, task_id, user = request.user)
            form = TaskForm(request.POST, instance= task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', { 'task':task, 'form':form, 'error':"error updating task"})
        
def task_complete(request, task_id):
    task = get_object_or_404(Task, task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

def task_delete(request, task_id):
    task = get_object_or_404(Task, task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm     
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
           try:
                # register user
                print(request.POST)
                user = User.objects.create_user(username=request.POST['username'], password= request.POST['password1'])
                user.save()
                # this login generate token(save of the sesion)
                login(request, user)
                return redirect('tasks')
                #return HttpResponse('User Created successfully')
           except IntegrityError:
               render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': 'the username already exists'
                })
           except:
                render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': 'Error in the data bases'
                })
        
        return HttpResponse('password do not match ')
        


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    
    else:
        
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
    
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'usermane or password not corret'
        })
            
        # this login generate token(save of the sesion)
        login(request, user)
        return redirect('tasks')
