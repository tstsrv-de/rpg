from django.db.models import deletion
from django.db.models.aggregates import Count
from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from rjh_rpg.models import UserChar
from rjh_rpg.forms import UserCharForm
from rjh_rpg.models import GameState
from rjh_rpg.models import GameScenes
from rjh_rpg.models import GameScenesRunning
from rjh_rpg.models import LobbySlots

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
                # (TODO!) should we delete gamesessions here?
                return redirect('home')
            else:
                return render (request,'login.html', {'error':'Benutzername oder Passwort falsch!'})
        else:
            return render(request,'login.html')

def logout(request):
    if request.user.is_authenticated:
        
        current_user_obj = User.objects.get(id=request.user.id)
        GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)

        user_char_list = UserChar.objects.filter(usernickname=current_user_obj)
        for user_char in user_char_list:
            try:
                LobbySlots.objects.get(user_char_id=user_char).delete()
            except:
                pass

        try:
            GameScenesRunning.objects.get(char=GameState_char_obj[0].char).delete()
        except:
            pass
        
        try:
            GameState.objects.get(char_user=current_user_obj).delete()
        except:
            pass
        

        auth.logout(request)

        return render(request,'msg_redirect.html',{'msg':'Du wurdest ausgelogt!'})
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})
        


def home(request):
    if request.user.is_authenticated:
        pass
    else:
        pass
    return render(request, 'home.html')


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'user_profile.html')
    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})


# game views and logic:

def chars(request):
    if request.user.is_authenticated:
        current_user_obj = User.objects.get(id=request.user.id)
        GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)
        try:
            GameScenesRunning.objects.get(char=GameState_char_obj[0].char).delete()
        except:
            pass
        try:
            GameState.objects.get(char_user=current_user_obj).delete()
        except:
            pass

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
 
    
def worldmap(request): # (TODO!) dringend zusammenkopierten kram aufräumen und zusammenpacken
    if request.user.is_authenticated:
        if request.method == 'POST':

            # (TODO!) manipulation von post daten möglich? oder ist das der csf-token? falls nicht: id gegen datenbank prüfen und fehler anzeigen, falls nicht vorhanden (und ggfls. nicht zum user passt)
            char_id = request.POST.get('char')

            # get user obj from logged in user
            current_user_obj = User.objects.get(id=request.user.id)

            # get gamestate obj based on the user object
            GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)

            # delete lobby slots
            user_char_list = UserChar.objects.filter(usernickname=current_user_obj)
            for user_char in user_char_list:
                try:
                    LobbySlots.objects.get(user_char_id=user_char).delete()
                except:
                    pass            
            

            char_from_db = UserChar.objects.get(id=char_id)
  
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
                
            char_name = char_from_db.name
            char_user = char_from_db.usernickname

            return render(request,
                'worldmap.html',
                {
                    'char_id': char_id,
                    'char_name' : char_name,
                    'char_user' : char_user,
                    'active_char_list' : active_char_list,
                    'game_scenes_list': complete_game_scenes_list,

                }
            )
        else: 
            # get user obj from logged in user
            current_user_obj = User.objects.get(id=request.user.id)

            # delete lobby slots
            user_char_list = UserChar.objects.filter(usernickname=current_user_obj)
            for user_char in user_char_list:
                try:
                    LobbySlots.objects.get(user_char_id=user_char).delete()
                except:
                    pass            


            # get gamestate obj based on the user object
            GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)

            # delete current running scenes to this char from current users gamestate
            char_id = GameState_char_obj[0].id

            try:
                GameScenesRunning.objects.get(char=GameState_char_obj[0].char).delete()
            except:
                pass
        
            # set char back to worldmap (place = 0)
            GameState.objects.filter(char=char_id).update(place=0)  

            # prepare nessesary lists for worldmap        
            active_char_list = GameState.objects.filter(place=0).order_by('char') # place 0 = worldmap
            game_scenes_list = GameScenes.objects.order_by('name') # place 0 = worldmap
            
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

            char_name = str(GameState_char_obj[0].char)
            char_user = str(GameState_char_obj[0].char_user)

            user_char_char_id = UserChar.objects.filter(name=char_name)
            
            char_id_form =  str(user_char_char_id[0].id)
            return render(request,
                'worldmap.html',
                {
                    'char_id': char_id_form,
                    'char_name' : char_name,
                    'char_user' : char_user,
                    'active_char_list' : active_char_list,
                    'game_scenes_list': complete_game_scenes_list,

                }
            )

    else:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

# from YT Chat howto
#def room(request, room_name):
#    return render(request, 'chatroom.html', {
#        'room_name': room_name
#    })

def scene(request):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})    
    if not request.method == 'POST':
        return render(request,'msg_redirect.html',{'msg':'Du musst eine Szene auswählen!','target':'/chars/'})

    # add logic for games...
    pass

    
def lobby_jumper(request):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})    
    
    if request.method == 'POST':
        scene_id = request.POST.get('scene_id')
        return redirect('/lobby-'+scene_id+'/')
    else:
        return render(request,'msg_redirect.html',{'msg':'Du musst eine Szene auswählen!','target':'/worldmap/'})    


def lobby(request, scene_id):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})    

    if not GameScenes.objects.filter(id=scene_id).exists():
        return render(request,'msg_redirect.html',{'msg':'Du musst eine existierende Szene auswählen!','target':'/worldmap/'})    
    
    current_user_obj = User.objects.get(id=request.user.id)
    GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)
    char_id = str(GameState_char_obj[0].char.id)

    # set char to the scene
    GameState.objects.filter(char=char_id).update(place=scene_id)  

    gs_obj = GameScenes.objects.filter(id=scene_id)            
    usr_obj = UserChar.objects.get(id=char_id)
    
    new_gsr = GameScenesRunning(char=usr_obj, scene_step=gs_obj[0].start_step, game_id=0 )
    new_gsr.save()
    
    char_name = str(usr_obj)


    return render(request,
        'lobby.html',
        {
            'char_id': char_id,
            'scene_id' : scene_id,
            'char_name' : char_name, 
        }
    )


