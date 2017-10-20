from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'loginRegistration/index.html')

def process(request):
    print request.POST
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_pw)
        request.session['id'] = user.id
        return redirect('/success')

def login(request):
    login_return = User.objects.login(request.POST)
    if(login_return == None):
        messages.error(request, login_return['error'])
        return redirect('/')
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        return redirect('/success')
    else: 
        print login_return['error']
        messages.error(request, login_return['error'])
        return redirect('/')

def success(request):
    context={
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'loginRegistration/success.html', context)


