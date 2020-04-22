from django.shortcuts import render, redirect, HttpResponse 
# Using Django Messages: https://docs.djangoproject.com/en/1.11/ref/contrib/messages/#displaying-messages 
from django.contrib import messages 
from .models import * 
import bcrypt
 
 
 
# Create your views here. 
def index(request): 
    return render(request, 'login_reg/index.html')

def register(request):
    
    reg_errors = User.objects.registration_validator(request.POST)

    #validate registration
    if len(reg_errors):
        for k, v in reg_errors.items():
            messages.error(request,v)
        return redirect('/')

    else:
        hashedPW = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pw_hash = hashedPW, date_of_birth=request.POST['dob'])
        request.session['cur_user'] = newUser.id
    return redirect('/welcome/')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    thisUser = User.objects.filter(email = request.POST["login_email"])
    #validate login
    if len(login_errors) or len(thisUser) <= 0:
        for k, v in login_errors.items():
            messages.info(request, v)
        return redirect('/')
    else:
        request.session['cur_user'] = thisUser.first().id
        return redirect('/welcome/')


def welcome(request):
    if not 'cur_user' in request.session:
        return redirect('/')
    else:
        thisUser = User.objects.get(id = request.session['cur_user'])
    context = {
        "user" : thisUser,
    }

    return render(request, 'login_reg/welcome.html', context)



def destroy(request):
    request.session.flush()
    return redirect('/')


def reg_ajax(request):
    # check email uniqueness

    emailExists = False
    allEmails = User.objects.filter(email=request.POST['email'])

    if len(allEmails) > 0:
        emailExists = True
    
    context = {
        "emailExists" : emailExists,
    }

    return render(request, 'login_reg/partials/unique_email.html', context)
















