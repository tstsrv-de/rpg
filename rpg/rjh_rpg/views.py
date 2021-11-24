from django.shortcuts import render

# Create your views here.

def index(request):
    return redirect('home')


from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from rjh_rpg.models import UserChar

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Benutzername ist bereits vergeben!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'signup.html', {'error':'Passwörter stimmen nicht überein!'})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request,'login.html', {'error':'Benutzername oder Passwort falsch!'})
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        pass
    else:
        pass
    return render(request, 'home.html')

def chars(request):
    char_list = UserChar.objects.order_by('name')

    #add post variant to add new chars
    return render(request, 'chars.html', {'chars': char_list})

def user_profile(request):
    return render(request, 'user_profile.html')
