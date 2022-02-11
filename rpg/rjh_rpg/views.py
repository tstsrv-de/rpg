from django.db.models import deletion
from django.db.models.aggregates import Count
from django.http import request, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from rjh_rpg.models import UserChar
from rjh_rpg.forms import UserCharForm
from rjh_rpg.models import GameState
from rjh_rpg.models import GameScenes
from rjh_rpg.models import LobbySlots
from rjh_rpg.models import Games
from rjh_rpg.models import UserCharInGames

from rjh_rpg.rpg_tools import rpg_user_has_active_game
from rjh_rpg.rpg_tools import rpg_user_is_player_of_this_game_id
from rjh_rpg.rpg_tools import rpg_get_config, rpg_user_char_id_to_name

from math import ceil

def signup(request):
    if request.user.is_authenticated:
        return render(request, 'msg_redirect.html', {
            'msg':'Du bist bereits angemeldet!', 
            'target':'/chars/'
            })
    else:
        if request.method == "POST":
            if request.POST['password1'] == request.POST['password2']:
                try:
                    User.objects.get(username = request.POST['username'])
                    return render (request,'signup.html', {'error':'Benutzername ist bereits vergeben!'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                    auth.login(request,user)
                    return render(request,'msg_redirect.html',{'msg':'Du wurdest erfolgreich angemeldet!','target':'/chars/'})
            else:
                return render (request,'signup.html', {'error':'Passwörter stimmen nicht überein!'})
        else:
            return render(request,'signup.html')

def login(request):
    if request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist bereits angemeldet!','target':'/chars/'})
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

def BOOchars(request, user_char_id=None):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

    if rpg_user_has_active_game(request.user) != 0: # 0 = no active game, <0 = running game_id 
        return render(request,'msg_redirect.html',{'msg':'Du hast noch ein aktives Spiel. Spiel erst fertig!','target':'/game-'+ str(rpg_user_has_active_game(request.user)) +'/'})
    
    current_user_obj = User.objects.get(id=request.user.id)
    GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)
    

    try:
        GameState.objects.get(char_user=current_user_obj).delete()
    except:
        pass

    char_list = UserChar.objects.filter(usernickname=request.user).order_by('name')
    
    current_user = User.objects.get(id=request.user.id)
    active_char = GameState.objects.filter(char_user=current_user)
    xp_to_ap_rate = rpg_get_config("xp_ap_conversion_factor")
    xp_to_hp_rate = rpg_get_config("xp_hp_conversion_factor")

    
    return render(request, 'chars.html', {'chars': char_list, 'active_char' : active_char, 'xp_ap' : xp_to_ap_rate, 'xp_hp' : xp_to_hp_rate })


def worldmap(request, char_id):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

    is_users_char = False
    curr_users_user_char_list = UserChar.objects.filter(usernickname=User.objects.get(id=request.user.id))
    for user_char in curr_users_user_char_list:
        if user_char.id == char_id:
            is_users_char = True
            
    if not is_users_char:
        return render(request,'msg_redirect.html',{'msg':'Dieser Charakter gehört dir nicht oder existiert nicht!','target':'/chars/'})

    if rpg_user_has_active_game(request.user) != 0: # 0 = no active game, <0 = running game_id 
        return render(request,'msg_redirect.html',{'msg':'Du hast noch ein aktives Spiel. Spiel erst fertig!','target':'/game-'+ str(rpg_user_has_active_game(request.user)) +'/'})
    
    char_to_gamestate = GameState()

    char_from_db = UserChar.objects.get(id=char_id)
    char_to_gamestate.char = char_from_db
    char_to_gamestate.place = 0

    current_user = User.objects.get(id=request.user.id)
    char_to_gamestate.char_user = current_user

   
    
    game_state_char_id = GameState.objects.filter(char = char_from_db).delete()

    
    obj, created = GameState.objects.filter(char = char_from_db).update_or_create(char = char_from_db, place = 0)
    #.update_or_create(char = char_from_db, place = 0)
    print ("obj:" + str(obj))
    print ("created:" + str(created))
    
    current_user_obj = User.objects.get(id=request.user.id)
    user_char_list = UserChar.objects.filter(usernickname=current_user_obj)
    for user_char in user_char_list:
        try:
            LobbySlots.objects.get(user_char_id=char_id).delete()
        except:
            pass            

    # get gamestate obj based on the user object
    GameState_char_obj = GameState.objects.filter(char=char_id)
    
    # prepare nessesary lists for worldmap        
    active_char_list = GameState.objects.filter(place=0).order_by('char') # place 0 = worldmap
    game_scenes_list = GameScenes.objects.order_by('name') 
    
    complete_game_scenes_list = []

    for scene in game_scenes_list: 

        players_in_chat = GameState.objects.filter(place=scene.id)

        players_in_chat_counter = 0
        for player_in_chat in players_in_chat:
            players_in_chat_counter = players_in_chat_counter + 1

        waiting_players = LobbySlots.objects.filter(game_scene_id=scene.id)

        player_counter = 0
        for waiting_player in waiting_players:
            player_counter = player_counter + 1
        
        complete_game_scenes_list.append({
            'name': scene.name,
            'req_players': scene.req_players,
            'waiting_players': player_counter,
            'players_in_chat_counter' : players_in_chat_counter,
            'id': scene.id,
            }
        )
        
    char_name = rpg_user_char_id_to_name(char_id)

    user_char_char_id = UserChar.objects.filter(name=char_name)
    
    char_id_form =  str(user_char_char_id[0].id)
    return render(request,
        'worldmap.html',
        {
            'char_id': char_id_form,
            'char_name' : char_name,
            'active_char_list' : active_char_list,
            'game_scenes_list': complete_game_scenes_list,

        }
    )
  
    


def lobby(request, scene_id, char_id):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})    

    if not GameScenes.objects.filter(id=scene_id).exists():
        return render(request,'msg_redirect.html',{'msg':'Du musst eine existierende Szene auswählen!','target':'/worldmap'+str(char_id)+'/'})
    
    if rpg_user_has_active_game(request.user) != 0: # 0 = no active game, <0 = running game_id 
        return render(request,'msg_redirect.html',{'msg':'Du hast noch ein aktives Spiel. Spiel erst fertig!','target':'/game-'+ str(rpg_user_has_active_game(request.user)) +'/'})

    is_users_char = False
    curr_users_user_char_list = UserChar.objects.filter(usernickname=User.objects.get(id=request.user.id))
    for user_char in curr_users_user_char_list:
        if user_char.id == char_id:
            is_users_char = True
            
    if not is_users_char:
        return render(request,'msg_redirect.html',{'msg':'Dieser Charakter gehört dir nicht oder existiert nicht!','target':'/chars/'})

    current_user_obj = User.objects.get(id=request.user.id)
    GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)
    
    # catch wierd timeout/reload error
    #try:
    #    char_id = str(GameState_char_obj[0].char.id)
    #except:
    #    return render(request,'msg_redirect.html',{'msg':'aaaaDu musst einen Charakter auswählen!','target':'/chars/'})

    scene_name = GameScenes.objects.get(id=scene_id).name
    intro_image_name = GameScenes.objects.get(id=scene_id).intro_image 
    intro_text = GameScenes.objects.get(id=scene_id).intro_text

    GameState.objects.filter(char=char_id).update(place=scene_id)

    usr_obj = UserChar.objects.get(id=char_id)

    char_name = str(usr_obj)

    return render(request, 'lobby.html', {
            'char_id': char_id,
            'scene_id': scene_id,
            'scene_name': scene_name,
            'char_name': char_name,
            'intro_image': intro_image_name,
            'intro_text': intro_text
        }
    )

def game(request, game_id):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})    

    if not Games.objects.filter(id=game_id).exists():
        return render(request,'msg_redirect.html',{'msg':'Das Spiel existiert nicht!','target':'/worldmap/'})
    
    game_obj = Games.objects.get(id=game_id)
    
    if game_obj.game_finished == True:
        return render(request,'msg_redirect.html',{'msg':'Das Spiel ist bereits beendet!','target':'/worldmap/'})

    if rpg_user_is_player_of_this_game_id(game_id, request.user) == False:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht Spieler dieses Spiels!','target':'/worldmap/'})
    
    # Checks done: 
    # - user is logged in
    # - game exists
    # - game is not finished
    # - user is player of this game
    

    game_scene = game_obj.game_scene_id
    scene_name = GameScenes.objects.get(name=game_scene).name
    image_name = GameScenes.objects.get(name=game_scene).enemy_image
    enemy_dead_image = GameScenes.objects.get(name=game_scene).enemy_dead_image
    enemy_name = GameScenes.objects.get(name=game_scene).enemy_name
    current_user_id = User.objects.get(id=request.user.id).id
    
    game_user_char_list = []
    for user_char in UserCharInGames.objects.filter(game_id=game_id).order_by('id'):
        user_char_details = UserChar.objects.get(name=user_char.user_char_id)
        game_user_char_list.append({
            'user_char_in_games_id': user_char.id,
            'name': user_char.user_char_id,
            'klasse': user_char_details.Klasse, 
            'geschlecht': user_char_details.Geschlecht,
            'hp': user_char_details.hp,
            'ap': user_char_details.ap,
            'user_char_id': user_char_details.usernickname.id,
            }
        )
    sorted_game_user_char_list = []  
    for user_char in game_user_char_list:
        if current_user_id == user_char['user_char_id']:
            sorted_game_user_char_list.insert(0,user_char)
        else:
            sorted_game_user_char_list.append(user_char)

    game_user_char_list = sorted_game_user_char_list

    
    if len(game_user_char_list) > 1:
        icon_size = ""
        font_size = ""
    else:
        icon_size = "font-size:4vw"
        font_size = "font-size:1vw"
    
    return render(request,'game.html', {
        'game_id': game_id,
        'game_user_char_list' : game_user_char_list,  
        'request_user_id'      : current_user_id,
        'enemy_image': image_name,
        'enemy_dead_image': enemy_dead_image,
        'enemy_name': enemy_name,
        'scene_name': scene_name, 
        'icon_size': icon_size,
        'font_size': font_size,
    })
 
def hpap(request, hpap, user_char_id):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

    if not UserChar.objects.filter(id=user_char_id).exists():
        return render(request,'msg_redirect.html',{'msg':'Dieser Charakter existiert nicht!','target':'/chars/'})
 
    is_users_char = False
    curr_users_user_char_list = UserChar.objects.filter(usernickname=User.objects.get(id=request.user.id))
    for user_char in curr_users_user_char_list:
        if user_char.id == user_char_id:
            is_users_char = True
            
    if not is_users_char:
        return render(request,'msg_redirect.html',{'msg':'Dieser Charakter gehört dir nicht!','target':'/chars/'})

    curr_xp = UserChar.objects.get(id=user_char_id).xp_to_spend
    if curr_xp >= 1:
        curr_xp_to_spend =  ceil(curr_xp * rpg_get_config("xp_to_spend_factor"))
        if hpap == "ap":
            curr_ap = UserChar.objects.get(id=user_char_id).ap
            new_ap = (curr_ap + ceil(curr_xp_to_spend * rpg_get_config("xp_ap_conversion_factor")))
            UserChar.objects.filter(id=user_char_id).update(xp_to_spend=(curr_xp - curr_xp_to_spend), ap=new_ap)
        elif hpap == "hp":
            curr_hp = UserChar.objects.get(id=user_char_id).hp
            new_hp = (curr_hp + ceil(curr_xp_to_spend * rpg_get_config("xp_hp_conversion_factor")))
            UserChar.objects.filter(id=user_char_id).update(xp_to_spend=(curr_xp - curr_xp_to_spend), hp=new_hp)
    return_string = "/chars/#" + str(user_char_id)
    return HttpResponseRedirect(return_string)
    #return redirect('chars')

def chars(request):
    if not request.user.is_authenticated:
        return render(request,'msg_redirect.html',{'msg':'Du bist nicht angemeldet!','target':'/login/'})

    if rpg_user_has_active_game(request.user) != 0: # 0 = no active game, <0 = running game_id 
        return render(request,'msg_redirect.html',{'msg':'Du hast noch ein aktives Spiel. Spiel erst fertig!','target':'/game-'+ str(rpg_user_has_active_game(request.user)) +'/'})

    current_user_obj = User.objects.get(id=request.user.id)
    GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)
    

    try:
        GameState.objects.get(char_user=current_user_obj).delete()
    except:
        pass

    char_list = UserChar.objects.filter(usernickname=request.user).order_by('name')
    
    current_user = User.objects.get(id=request.user.id)
    active_char = GameState.objects.filter(char_user=current_user)
    xp_to_ap_rate = rpg_get_config("xp_ap_conversion_factor")
    xp_to_hp_rate = rpg_get_config("xp_hp_conversion_factor")

    form = UserCharForm()
    
    if request.method == 'POST':
        form = UserCharForm(request.POST)
        if form.is_valid():
            tmp_form = form.save(commit=False)
            tmp_form.usernickname = request.user
            if tmp_form.Klasse == "W":
                tmp_form.hp = rpg_get_config("char_class_w_base_hp")
                tmp_form.ap = rpg_get_config("char_class_w_base_ap")
            elif tmp_form.Klasse == "P":
                tmp_form.hp = rpg_get_config("char_class_p_base_hp")
                tmp_form.ap = rpg_get_config("char_class_p_base_ap")
            elif tmp_form.Klasse == "M":
                tmp_form.hp = rpg_get_config("char_class_m_base_hp")
                tmp_form.ap = rpg_get_config("char_class_m_base_ap")
            else:
                # should not happen
                pass
                

            tmp_form.save()
            return render(request,'msg_redirect.html',{'msg':'Der Char wurde erfolgreich angelegt!','target':'/chars/'})
        else:
            return render(request,'msg_redirect.html',{'msg':'Fehler bei der Charaktererstellung. Versuche es bitte noch mal!','target':'/chars/'})


    current_user_obj = User.objects.get(id=request.user.id)
    GameState_char_obj = GameState.objects.filter(char_user=current_user_obj)
    

    try:
        GameState.objects.get(char_user=current_user_obj).delete()
    except:
        pass

    char_list = UserChar.objects.filter(usernickname=request.user).order_by('name')
    
    current_user = User.objects.get(id=request.user.id)
    active_char = GameState.objects.filter(char_user=current_user)
    xp_to_ap_rate = rpg_get_config("xp_ap_conversion_factor")
    xp_to_hp_rate = rpg_get_config("xp_hp_conversion_factor")

    
    
    return render(request, 'chars.html', {
        'chars': char_list, 
        'form': form, 
        'active_char' : active_char, 
        'xp_ap' : xp_to_ap_rate, 
        'xp_hp' : xp_to_hp_rate 
        })
