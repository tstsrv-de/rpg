from django.db.models.aggregates import Count
from django.shortcuts import render

# Create your views here.

def index(request):
    return redirect('home')


from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from rjh_rpg.models import UserChar
from rjh_rpg.forms import UserCharForm
from rjh_rpg.models import GameState

def signup(request):
    if request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist bereits angemeldet!','target':'/user_profile/'})
    else:
        if request.method == "POST":
            if request.POST['password1'] == request.POST['password2']:
                try:
                    User.objects.get(username = request.POST['username'])
                    return render (request,'signup.html', {'error':'Benutzername ist bereits vergeben!'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                    auth.login(request,user)
                    return render(request,'msg_redirect.html',{'msg':'Du wurdest erfolgreich angemeldet!','target':'/user_profile/'})
            else:
                return render (request,'signup.html', {'error':'Passwörter stimmen nicht überein!'})
        else:
            return render(request,'signup.html')

def login(request):
    if request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist bereits angemeldet!','target':'/user_profile/'})
    else:
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
    if request.user.is_authenticated:
        auth.logout(request)
        # (TODO!) Alles Chars aus GameState löschen!
        return render(request,'msg_redirect.html',{'msg':'Du wurdest ausgelogt!'})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})
        


def home(request):
    if request.user.is_authenticated:
        pass
    else:
        pass
    return render(request, 'home.html')

def chars(request):
    if request.user.is_authenticated:
        char_list = UserChar.objects.filter(usernickname=request.user).order_by('name')
        form = UserCharForm()
        
        if request.method == 'POST':
            form = UserCharForm(request.POST)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.usernickname = request.user
                tmp_form.save()
                return render(request,'msg_redirect.html',{'msg':'Der Char wurde erfolgreich angelegt!','target':'/chars/'})
            else:
                pass
        
        return render(request, 'chars.html', {'chars': char_list, 'form': form})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'user_profile.html')
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})


# game views and logic:

def game_worldmap(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            # (TODO!) manipulation von post daten möglich? oder ist das der csf-token? falls nicht: id gegen datenbank prüfen und fehler anzeigen, falls nicht vorhanden (und ggfls. nicht zum user passt)
            char_id = request.POST.get('char')

            char_from_db = UserChar.objects.get(id=char_id)
            char_name = char_from_db.name
            char_user = char_from_db.usernickname
            
            char_to_gamestate = GameState()
            char_to_gamestate.char = char_from_db
            current_user = User.objects.get(id=request.user.id)
            char_to_gamestate.char_user = current_user

            try_active_char = GameState.objects.filter(char=char_from_db)
            try_active_user = GameState.objects.filter(char_user=current_user)
    
            if (try_active_user.count != 0) or (try_active_char.count != 0):
                return render(request,'msg_redirect.html',{'msg':'Du bist schon mit einem Char auf der Worldmap!','target':'/chars/'})
            else:
                char_to_gamestate.save()

            return render(request,
                'game_worldmap.html',
                {
                    'char_id': char_id,
                    'char_name' : char_name,
                    'char_user' : char_user,

                }
            )
        else: 
            return render(request,'msg_redirect.html',{'msg':'Du musst einen Char auswählen!','target':'/chars/'})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})
