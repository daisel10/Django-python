from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    
    if request.method == 'GET':
        print('enviando datos')
    else:
        if request.POST['password1'] == request.POST['password2']:
           try:
                # register user
                print(request.POST)
                user = User.objects.create_user(username=request.POST['username'], password= request.POST['password1'])
                user.save()
                # this login generate token
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
        
    #return render(request, 'signup.html',{
     #   'form': UserCreationForm     
      #   })
    
def tasks(request):
    return render(request, 'tasks.html')