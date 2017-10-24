from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login1/index.html')

def processreg(request):
    postData = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm_password': request.POST['confirm_password'],
    }
    errors = User.objects.validate_reg(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['first_name'] = postData['first_name']
        return redirect('/success')
    else:
        for error in errors:
            messages.info(request, error)
        return redirect('/')

def processlog(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    errors = User.objects.validate_log(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['first_name'] = User.objects.filter(email=postData['email'])[0].first_name
        return redirect('/success')
    for error in errors:
        messages.info(request, error)
    return redirect('/')

def success(request):
    context = {
        'users' : User.objects.all()
    }
    return render(request, 'login1/success.html', context)