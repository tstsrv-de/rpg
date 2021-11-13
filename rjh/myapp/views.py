from django.shortcuts import render
from django.http import HttpResponse

from myapp.models import Webpage, Topic, AccessRecord, User

def index(request):
    ar_list = AccessRecord.objects.order_by('date')

    frontend_values = {
        'test_variable': 'Das kommt aus der View-Datei!',
        'access_records': ar_list
    }

    return render(request, 'myapp/main.html', context=frontend_values)


def get_users(request):
    user_list = User.objects.all()

    frontend_values = {
        'users': user_list
    }
    return render(request, 'myapp/users.html', context=frontend_values)


def rjhapp(request):
    
    return render(request, 'myapp/rjhapp.html')

