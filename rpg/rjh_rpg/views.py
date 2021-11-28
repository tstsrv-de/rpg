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
from rjh_rpg.models import GameScenes
from rjh_rpg.models import GameScenesRunning

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

        current_user = User.objects.get(id=request.user.id)
        GameState.objects.get(char_user=current_user).delete()

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
        
        current_user = User.objects.get(id=request.user.id)
        active_char = GameState.objects.filter(char_user=current_user)

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
        
        return render(request, 'chars.html', {'chars': char_list, 'form': form, 'active_char' : active_char})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'user_profile.html')
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})


# game views and logic:

def game_stopsession(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        GameState.objects.get(char_user=current_user).delete()
        return render(request,'msg_redirect.html',{'msg':'Deine Chars wurden zurückgesetzt!','target':'/chars/'})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})
    
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

            no_active_char = False
            no_active_user = False

            try: # user ist mit diesem char aktiv
                try_active_char = GameState.objects.get(char=char_from_db)
            except:
                no_active_char = True

            try: # = user ist mit anderem char aktiv
                try_active_user = GameState.objects.get(char_user=current_user)
            except:
                no_active_user = True

            if no_active_char and no_active_user: # = new user on map
                char_to_gamestate.save()
            else:
                return render(request,'msg_redirect.html',{'msg':'Du bist schon mit einem Char auf der Worldmap!','target':'/chars/'})

            active_char_list = GameState.objects.filter(place=0).order_by('char') # place 0 = worldmap
            
            game_scenes_list = GameScenes.objects.order_by('name') # place 0 = worldmap
            
            # laufende szenen
            
            # wartende spieler in start steps
            
            complete_game_scenes_list = []

                        
            for scene in game_scenes_list: 
                waiting_players = GameScenesRunning.objects.filter(scene_step=scene.start_step)

                player_counter = 0
                for waiting_player in waiting_players:
                    player_counter = player_counter + 1
                
                
                complete_game_scenes_list.append({
                    'name': scene.name,
                    'req_players': scene.req_players,
                    'waiting_players': player_counter,
                    'id': scene.id,
                    }
                )
           

            return render(request,
                'game_worldmap.html',
                {
                    'char_id': char_id,
                    'char_name' : char_name,
                    'char_user' : char_user,
                    'active_char_list' : active_char_list,
                    'game_scenes_list': complete_game_scenes_list,

                }
            )
        else: 
            return render(request,'msg_redirect.html',{'msg':'Du musst einen Char auswählen!','target':'/chars/'})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

# from YT Chat howto
def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })

def game_scene(request):
    if request.user.is_authenticated:

        if request.method == 'POST':

            # (TODO!) manipulation von post daten möglich? oder ist das der csf-token? falls nicht: id gegen datenbank prüfen und fehler anzeigen, falls nicht vorhanden (und ggfls. nicht zum user passt)
            scene_id = request.POST.get('scene_id')
            char_id = request.POST.get('char_id')
            
            GameState.objects.filter(char=char_id).update(place=scene_id)  

            gs_obj = GameScenes.objects.filter(id=scene_id)            
            usr_obj = UserChar.objects.get(id=char_id)
            
            new_gsr = GameScenesRunning(char=usr_obj, scene_step=gs_obj[0].start_step, game_id=0 )
            new_gsr.save()


            return render(request,
                'game_scene.html',
                {
                    'char_id': char_id,
                    'scene_id' : scene_id,
                    
                }
            )
        else: 
            return render(request,'msg_redirect.html',{'msg':'Du musst eine Szene auswählen!','target':'/chars/'})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})    
    
